import os
import json
import base64
import zipfile
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import FileResponse
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from src.utils.processor import FloorPlanProcessor


# Base directory for all uploaded files
BASE_UPLOAD_DIRECTORY = "/home/cadian/project/ai_ce_main/receive_data"
PROCESSED_IMAGES_FILE = "processed_images.json"
INFERENCE_RESULTS_FILE = "inference_results.json"
LOG_FILE = "server.log"

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI()


class FileManager:
    """Handles file management, loading, saving, and directory creation."""

    @staticmethod
    def load_json_data(filename):
        """Load JSON data from a file."""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return {}

    @staticmethod
    def save_json_data(filename, data):
        """Save JSON data to a file."""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def create_directory(path):
        """Create a directory if it does not exist."""
        os.makedirs(path, exist_ok=True)


class ImageProcessor:
    """Encapsulates the image processing logic."""
    
    def __init__(self, processor=None):
        self.processor = processor or self._initialize_processor()
        self.executor = ThreadPoolExecutor(max_workers=5)

    @staticmethod
    def _initialize_processor():
        """Initialize the FloorPlanProcessor with its configuration."""
        config = {
            'background_crop_model_path': './models/best_crop.pt',
            'segmentation_model_path': './models/best_segmentation.pt',
            'detection_model_paths': ['./models/best_detection.pt'],
            'oob_model_path': './models/best_oob.pt',
            'segmentation_classes': [
                'wall', 'bed_room', 'bathroom', 'others', 'balcony', 'stairs',
                'living_kitchen', 'entrance', 'utility_room', 'air_room',
                'elevator', 'pantry', 'dressing_room', 'hallway'
            ],
            'detection_classes': [
                'basin', 'bathtub', 'commode', 'door_dwouble', 'door_hinged',
                'door_normal', 'elevator', 'gas', 'junc_I', 'junc_L', 'junc_T',
                'junc_X', 'sink', 'stairs', 'window'
            ],
            'oob_classes': ['wall']
        }
        return FloorPlanProcessor(config)

    def process_images(self, user_id, project_number, floor_number, image_base_name, images_dir):
        """Process images using the FloorPlanProcessor."""
        image_folder = os.path.dirname(images_dir)
        save_json_dir = os.path.join(image_folder, 'json')
        save_image_dir = os.path.join(image_folder, 'images')
        crop_image_dir = os.path.join(image_folder, 'cropped')

        # Create necessary directories
        FileManager.create_directory(save_json_dir)
        FileManager.create_directory(save_image_dir)
        FileManager.create_directory(crop_image_dir)

        processed_files = []

        for image_name in os.listdir(images_dir):
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                logger.info(f"Processing image: {image_name} for user: {user_id}")
                if not InferenceManager.is_image_processed(user_id, project_number, floor_number, image_name):
                    try:
                        self.processor.process_image(image_name, crop_image_dir, save_json_dir, save_image_dir)
                        InferenceManager.log_image_as_processed(user_id, project_number, floor_number, image_name)
                        logger.info(f"Successfully processed image: {image_name}")
                        processed_files.append(os.path.splitext(image_name)[0])
                    except Exception as e:
                        logger.error(f"Error processing image {image_name}: {e}")
                        raise e
                else:
                    logger.info(f"Image {image_name} was already processed.")
                    processed_files.append(os.path.splitext(image_name)[0])
        return processed_files

class InferenceManager:
    """Handles image processing status and inference result storage."""

    @staticmethod
    def is_image_processed(user_id, project_number, floor_number, image_name):
        """Check if a specific image has already been processed."""
        processed_images = FileManager.load_json_data(PROCESSED_IMAGES_FILE)
        return (
            user_id in processed_images and
            project_number in processed_images[user_id] and
            floor_number in processed_images[user_id][project_number] and
            image_name in processed_images[user_id][project_number][floor_number]
        )

    @staticmethod
    def log_image_as_processed(user_id, project_number, floor_number, image_name):
        """Mark an image as processed by recording it."""
        processed_images = FileManager.load_json_data(PROCESSED_IMAGES_FILE)
        if user_id not in processed_images:
            processed_images[user_id] = {}
        if project_number not in processed_images[user_id]:
            processed_images[user_id][project_number] = {}
        floor_key = f"floor_{floor_number}"
        if floor_key not in processed_images[user_id][project_number]:
            processed_images[user_id][project_number][floor_key] = []
        processed_images[user_id][project_number][floor_key].append(image_name)
        FileManager.save_json_data(PROCESSED_IMAGES_FILE, processed_images)

    @staticmethod
    def post_inference_results(user_id, project_number, floor_number, image_name):
        """Prepare and return inference results for a specific image."""
        image_base_name = os.path.splitext(image_name)[0]
        image_folder = os.path.join(BASE_UPLOAD_DIRECTORY, user_id, project_number, f"floor_{floor_number}", image_base_name)

        result_files = {
            "detection_json": os.path.join(image_folder, 'json', 'detect', f"{image_base_name}_detection.json"),
            "oob_json": os.path.join(image_folder, 'json', 'oob', f"{image_base_name}_oob.json"),
            "segmentation_json": os.path.join(image_folder, 'json', 'segment', f"{image_base_name}_segment.json"),
            "cropped_json": os.path.join(image_folder, 'json', 'crop', f"{image_base_name}.json"),
            "result_image": os.path.join(image_folder, 'images', f"{image_name}"),
            "original_image": os.path.join(image_folder, 'original_img', f"{image_name}"),
            "cropped_image": os.path.join(image_folder, 'cropped', f"{image_base_name}.png"),
        }

        encoded_files = {}
        filenames = {}
        for key, file_path in result_files.items():
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    encoded_files[key] = base64.b64encode(file.read()).decode('utf-8')
                    filenames[key] = os.path.basename(file_path)
            else:
                logger.warning(f"File not found: {file_path}. Skipping {key}.")
        if not encoded_files:
            logger.error(f"No files were found for image {image_name}.")
        InferenceManager.store_inference_results(user_id, project_number, floor_number, image_name, filenames)
        return {"message": "Inference results ready", "user_id": user_id, "project_number": project_number, "floor_number": floor_number, "image_name": image_name}

    @staticmethod
    def store_inference_results(user_id, project_number, floor_number, image_name, filenames):
        """Store inference results for the user."""
        inference_results = FileManager.load_json_data(INFERENCE_RESULTS_FILE)
        if user_id not in inference_results:
            inference_results[user_id] = []
        inference_results[user_id].append({
            "project_number": project_number,
            "floor_number": floor_number,
            "image_name": image_name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filenames": filenames
        })
        FileManager.save_json_data(INFERENCE_RESULTS_FILE, inference_results)

@app.post("/receive_data")
async def upload_file(
    request: Request,  
    images: UploadFile = File(...),
):
    """Handle file uploads, process them, and dynamically handle extra form fields."""
    image_processor = ImageProcessor()

    try:
        # Parse all form data dynamically
        form_data = await request.form()

        # Extract required fields from the form
        user_id = form_data.get('user_id')
        project_number = form_data.get('project_number')
        floor_number = form_data.get('floor_number')

        # Validate required fields (date field is now removed)
        if not all([user_id, project_number, floor_number]):
            missing_fields = [field for field in ['user_id', 'project_number', 'floor_number'] if form_data.get(field) is None]
            raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")

        # Handle extra dynamic fields
        extra_fields = {key: value for key, value in form_data.items() if key not in {'user_id', 'project_number', 'floor_number'}}
        
        if extra_fields:
            logger.info(f"Received extra fields: {extra_fields}")

        # Continue with image upload and processing
        user_directory = os.path.join(BASE_UPLOAD_DIRECTORY, user_id)
        project_directory = os.path.join(user_directory, project_number)
        floor_directory = os.path.join(project_directory, f"floor_{floor_number}")

        # Prepare new directories
        original_filename, file_extension = os.path.splitext(images.filename)
        image_folder = os.path.join(floor_directory, original_filename)
        FileManager.create_directory(image_folder)

        original_img_directory = os.path.join(image_folder, "original_img")
        FileManager.create_directory(original_img_directory)
        file_location = os.path.join(original_img_directory, f"{original_filename}{file_extension}")

        # Save the uploaded image file
        with open(file_location, "wb") as file:
            file.write(await images.read())

        # Process the image in a separate thread
        future = image_processor.executor.submit(image_processor.process_images, user_id, project_number, floor_number, original_filename, original_img_directory)
        processed_files = future.result()

        if original_filename not in processed_files:
            raise HTTPException(status_code=500, detail="File processing failed")

        # Prepare the response data
        response_data = InferenceManager.post_inference_results(user_id, project_number, floor_number, f"{original_filename}{file_extension}")

        # Track the new files created during this request
        new_files_to_zip = []

        # Only include files that were processed during the current request in the ZIP
        for processed_file in processed_files:
            json_path = os.path.join(floor_directory, processed_file, 'json')
            image_path = os.path.join(floor_directory, processed_file, 'images')
            cropped_path = os.path.join(floor_directory, processed_file, 'cropped')
            original_img_path = os.path.join(floor_directory, processed_file, 'original_img')

            # Add relevant files to the list for zipping
            for folder in [json_path, image_path, cropped_path, original_img_path]:  # Now includes original images folder
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        full_path = os.path.join(root, file)
                        new_files_to_zip.append(full_path)  # Track files created in this request

        # Create a ZIP archive of only the newly processed files, including original images
        zip_filename = f"{user_id}_{project_number}_floor_{floor_number}_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
        zip_file_path = os.path.join(BASE_UPLOAD_DIRECTORY, zip_filename)

        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file_path in new_files_to_zip:
                rel_path = os.path.relpath(file_path, os.path.join(BASE_UPLOAD_DIRECTORY, user_id))
                zipf.write(file_path, arcname=os.path.join(user_id, rel_path))

        return FileResponse(zip_file_path, media_type='application/zip', filename=zip_filename)
    
    except HTTPException as e:
        logger.error(f"HTTP Error: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error during file upload and processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    """Endpoint for checking the health status of the server."""
    return {"status": "healthy"}

# Manage server startup and shutdown
@asynccontextmanager
async def lifespan(app):
    """Manage the server's startup and shutdown events."""
    logger.info("Server starting up")
    yield
    logger.info("Server shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port= your port)
