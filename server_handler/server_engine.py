import os
import json
import base64
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
# Import the FloorPlanProcessor from the correct module, ensuring it handles image processing
from src.utils.processor import FloorPlanProcessor # this is from AI model module


# Base directory for all uploaded files
BASE_UPLOAD_DIRECTORY = "/home/cadian/project/ai_ce_main/receive_data"

# File to track processed images and inference results
PROCESSED_IMAGES_FILE = "processed_images.json"
INFERENCE_RESULTS_FILE = "inference_results.json"

# Initialize the FastAPI app
app = FastAPI()

# Set up logging to track server activity
log_file = "server.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize processor and thread pool for asynchronous processing
processor = None
executor = ThreadPoolExecutor(max_workers=5)

def initialize_processor():
    """Initialize the FloorPlanProcessor for handling image processing."""
    global processor # Ensure the processor is a global variable
    if processor is None:
        # Define the configuration for different models and classes for detection and segmentation
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
        processor = FloorPlanProcessor(config)  # Initialize the processor with the configuration

# Utility functions to load and save data from JSON files
def load_json_data(filename):
    """Load JSON data from a file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_json_data(filename, data):
    """Save JSON data to a file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
# Check and log processed images
def is_image_processed(user_id, project_number, floor_number, image_name):
    """Check if a specific image has already been processed."""
    processed_images = load_json_data(PROCESSED_IMAGES_FILE)
    return (
        user_id in processed_images and 
        project_number in processed_images[user_id] and 
        floor_number in processed_images[user_id][project_number] and 
        image_name in processed_images[user_id][project_number][floor_number]
    )

def log_image_as_processed(user_id, project_number, floor_number, image_name):
    """Mark an image as processed by recording it in the processed images file."""
    processed_images = load_json_data(PROCESSED_IMAGES_FILE)
    if user_id not in processed_images:
        processed_images[user_id] = {}
    if project_number not in processed_images[user_id]:
        processed_images[user_id][project_number] = {}
    floor_key = f"floor_{floor_number}"
    if floor_key not in processed_images[user_id][project_number]:
        processed_images[user_id][project_number][floor_key] = []
    if image_name not in processed_images[user_id][project_number][floor_key]:
        processed_images[user_id][project_number][floor_key].append(image_name)
    save_json_data(PROCESSED_IMAGES_FILE, processed_images)
    
# Encode files to base64 for transmission. It is important to encode the files before sending them back to the client.
def encode_file_to_base64(file_path: str) -> str:
    """Read a file and encode it in base64 format."""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')
# Post processed inference results for user
def post_inference_results(user_id, project_number, floor_number, image_name):
    """
    Prepare and encode the processed files for a specific user, project, and image.
    The files are returned as base64 encoded data ready for transmission.
    """
    image_base_name = os.path.splitext(image_name)[0]
    image_folder = os.path.join(BASE_UPLOAD_DIRECTORY, user_id, project_number, f"floor_{floor_number}", image_base_name)

    # Define where the various processed files should be stored
    result_files = {
        "detection_json": os.path.join(image_folder, 'json', 'detect', f"{image_base_name}_detection.json"),
        "oob_json": os.path.join(image_folder, 'json', 'oob', f"{image_base_name}_oob.json"),
        "segmentation_json": os.path.join(image_folder, 'json', 'segment', f"{image_base_name}_segment.json"),
        "cropped_json": os.path.join(image_folder, 'json', 'crop', f"{image_base_name}.json"),
        "result_image": os.path.join(image_folder, 'images', f"{image_name}"),
        "original_image": os.path.join(image_folder, 'original_img', f"{image_name}"),
        "cropped_image": os.path.join(image_folder, 'cropped', f"{image_base_name}.png"),
    }
    try:
        encoded_files = {}
        filenames = {}
        # Encode each file in base64 and store it in the encoded_files dictionary
        for key, file_path in result_files.items():
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    encoded_files[key] = base64.b64encode(file.read()).decode('utf-8')
                    filenames[key] = os.path.basename(file_path)  # Get the filename for tracking
            else:
                logger.warning(f"File not found: {file_path}. Skipping {key}.")
        if not encoded_files:
            logger.error(f"No files were found to send for image {image_name}.")
        # Append the results to the INFERENCE_RESULTS_FILE for the given user
        inference_results = load_json_data(INFERENCE_RESULTS_FILE)
        if user_id not in inference_results:
            inference_results[user_id] = []
        # This will store the results for the user, project, floor, and image in the INFERENCE_RESULTS_FILE
        inference_results[user_id].append({
            "project_number": project_number,
            "floor_number": floor_number,
            "image_name": image_name,
            "files": encoded_files,
            "filenames": filenames
        })
        save_json_data(INFERENCE_RESULTS_FILE, inference_results)
        # Response to the client that the inference results are ready
        return JSONResponse(
            content={
                "message": "Inference results ready",
                "user_id": user_id,
                "project_number": project_number,
                "floor_number": floor_number,
                "image_name": image_name
            },
            status_code=200 # status code 200 indicates success
        )
    except Exception as e:
        error_message = f"Unexpected error processing files for {image_name}: {str(e)}"
        logger.error(error_message)
        return JSONResponse(status_code=500, content={"message": error_message})

# New global variable to keep track of sent results and last retrievals
sent_results = {}
last_retrieval_time = {}
# Retrieve inference results for a specific user

@app.get("/get_inference_results/{user_id}")
async def get_inference_results(user_id: str):
    """
    Retrieve the inference results for a given user.
    Once retrieved, the results are marked as sent, and future retrievals will not resend the same results.
    """    
    try:
        inference_results = load_json_data(INFERENCE_RESULTS_FILE)
        
        if user_id in inference_results and inference_results[user_id]:
            user_results = inference_results[user_id]
            
            # Clear the results for this user after sending
            if user_id not in last_retrieval_time:
                last_retrieval_time[user_id] = datetime.now()

            # Store the sent results for tracking and mark retrieval time
            sent_results[user_id] = user_results
            last_retrieval_time[user_id] = datetime.now()

            # Clear results only after they are retrieved
            inference_results[user_id] = []
            save_json_data(INFERENCE_RESULTS_FILE, inference_results)
            
            return JSONResponse(content=user_results, status_code=200)
        else:
            return JSONResponse(content={"message": "No new inference results available"}, status_code=204)
    except Exception as e:
        logger.error(f"Error retrieving inference results for user {user_id}: {str(e)}")
        return JSONResponse(content={"message": f"Error retrieving inference results: {str(e)}"}, status_code=500)

@app.get("/get_users_with_results")
async def get_users_with_results():
    """
    Return a list of users who currently have inference results pending.
    This endpoint helps the client dynamically fetch users that have results available.
    """
    try:
        inference_results = load_json_data(INFERENCE_RESULTS_FILE)
        users_with_results = [user_id for user_id, results in inference_results.items() if results]
        #logger.info(f"Users with results: {users_with_results}")
        return JSONResponse(content={"users_with_results": users_with_results}, status_code=200)
    except Exception as e:
        logger.error(f"Error retrieving users with results: {str(e)}")
        return JSONResponse(content={"message": f"Error retrieving users with results: {str(e)}"}, status_code=500)

# Upload and process images sent by the client
@app.post("/receive_data")
async def upload_file(
    user_id: str = Form(...),
    project_number: str = Form(...),
    floor_number: str = Form(...),
    date: str = Form(...),
    images: UploadFile = File(...)
):
    """
    Handle file uploads from the client, including processing and saving images.
    Results are generated based on the uploaded images and stored in the appropriate directories.
    """    
    try:
        # Initialize the processor to handle image-related tasks
        initialize_processor()

        # Define the directory structure based on the user, project, and floor numbers
        user_directory = os.path.join(BASE_UPLOAD_DIRECTORY, user_id)
        project_directory = os.path.join(user_directory, project_number)
        floor_directory = os.path.join(project_directory, f"floor_{floor_number}")

        # Create a timestamp for the file to make sure each file is unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Split the original filename and its extension
        original_filename, file_extension = os.path.splitext(images.filename)
        
        # Create a folder based on the original filename and timestamp (excluding the extension)
        folder_name = f"{original_filename}_{timestamp}"

        # Create the full directory path to save the file
        image_folder = os.path.join(floor_directory, folder_name)
        os.makedirs(image_folder, exist_ok=True)

        # Create a subdirectory for the original image
        original_img_directory = os.path.join(image_folder, "original_img")
        os.makedirs(original_img_directory, exist_ok=True)

        # Save the uploaded image
        filename = f"{original_filename}_{timestamp}{file_extension}"
        file_location = os.path.join(original_img_directory, filename)
        
        with open(file_location, "wb") as file:
            file.write(await images.read())

        # Process the uploaded file asynchronously using a thread pool
        future = executor.submit(process_user_data, user_id, project_number, floor_number, folder_name, original_img_directory)
        processed_files = future.result()

        if filename not in processed_files:
            raise HTTPException(status_code=500, detail="File processing failed")

        # Send back the inference results after processing
        response_data = post_inference_results(user_id, project_number, floor_number, filename)
        
        return response_data

    except Exception as e:
        logger.error(f"Error during file upload and processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Handle image processing and saving results
def process_user_data(user_id, project_number, floor_number, image_base_name, images_dir):
    """
    Process images using the FloorPlanProcessor and store the processed data.
    Results include segmentation, detection, and cropping.
    """
    image_folder = os.path.dirname(images_dir)
    save_json_dir = os.path.join(image_folder, 'json')
    save_image_dir = os.path.join(image_folder, 'images')
    crop_image_dir = os.path.join(image_folder, 'cropped')

    # Ensure that the necessary directories exist for storing processed data
    os.makedirs(save_json_dir, exist_ok=True)
    os.makedirs(save_image_dir, exist_ok=True)
    os.makedirs(crop_image_dir, exist_ok=True)

    processed_files = []
    
    # Process each image in the directory
    for image_name in os.listdir(images_dir):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            #logger.info(f"Processing image {image_name}...")
            if not is_image_processed(user_id, project_number, floor_number, image_name):
                try:
                    # Call the processor to generate the necessary results
                    #logger.info(f"Saving JSON files to {save_json_dir}, images to {save_image_dir}, and cropped images to {crop_image_dir}")
                    processor.process_image(image_name, crop_image_dir, save_json_dir, save_image_dir)
                    #logger.info(f"Processed and saved image: {image_name}")
                    
                    # Mark the image as processed
                    log_image_as_processed(user_id, project_number, floor_number, image_name)
                    processed_files.append(image_name)
                except Exception as e:
                    logger.error(f"Error processing image {image_name}: {e}")
                    raise e
            else:
                logger.info(f"Image {image_name} was already processed.")
                processed_files.append(image_name)
    
    return processed_files

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
