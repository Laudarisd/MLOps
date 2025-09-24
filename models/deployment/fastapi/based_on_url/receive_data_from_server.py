import os
import json
import base64
import requests
import logging
from logging.handlers import RotatingFileHandler

# Constants
BASE_SAVE_DIRECTORY = "./received_inference_results"
SERVER_URL = "http://your ip:8000"  # Replace with your server's URL and port

# Set up logging
log_file = "client_receiver.log"
logging.basicConfig(
    level=logging.DEBUG,  # Enable detailed logging
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def save_file(file_content_base64, save_path):
    """Save base64 encoded file content to disk."""
    try:
        #logger.info(f"Attempting to save file at {save_path}")
        file_content = base64.b64decode(file_content_base64)
        logger.debug(f"Decoded base64 content, length: {len(file_content)} bytes")
        
        # Ensure the directory exists
        directory = os.path.dirname(save_path)
        os.makedirs(directory, exist_ok=True)
        
        # Save the file
        with open(save_path, "wb") as f:
            f.write(file_content)
        #logger.info(f"Successfully saved file at {save_path}")
        
        # Verify the file was saved correctly
        if os.path.exists(save_path):
            logger.info(f"File verified at {save_path}")
        else:
            logger.error(f"File not found at {save_path} after saving attempt")
    except Exception as e:
        logger.error(f"Error saving file at {save_path}: {str(e)}")
        logger.exception("Detailed error information:")

def process_inference_result(user_id, result):
    """Process a single inference result and save its files."""
    try:
        #logger.info(f"Processing inference result for user {user_id}")
        #logger.debug(f"Result content: {result}")
        
        project_number = result.get('project_number')
        floor_number = result.get('floor_number')
        image_name = result.get('image_name')
        files = result.get('files', {})
        filenames = result.get('filenames', {})

        if not all([project_number, floor_number, image_name]):
            logger.error(f"Missing required information in result: {result}")
            return

        if not files:
            logger.error(f"No files received for image: {image_name}. Skipping processing.")
            return  # Skip further processing if no files are available
        
        base_path = BASE_SAVE_DIRECTORY
        
        # Loop through all the files received and save them dynamically
        for key, file_content_base64 in files.items():
            if key in filenames:
                filename = filenames[key]
                # Dynamically save the file in the corresponding folder structure
                save_path = os.path.join(base_path, user_id, project_number, f"floor_{floor_number}", os.path.splitext(image_name)[0], key, filename)
                #logger.info(f"Saving file: {key} as {filename}")
                save_file(file_content_base64, save_path)
            else:
                logger.warning(f"Filename not found for key {key}")
        
        logger.info(f"Processed and saved files for user: {user_id}, project: {project_number}, floor: {floor_number}, image: {image_name}")
    except Exception as e:
        logger.error(f"Error processing inference result: {str(e)}")
        logger.error(f"Problematic result: {result}")
        logger.exception("Detailed error information:")

def receive_inference_results(user_id):
    """Receive historical inference results for a specific user."""
    try:
        url = f"{SERVER_URL}/get_inference_results/{user_id}"  # Construct URL with user_id
        #logger.info(f"Requesting inference results from server for user {user_id}: {url}")
        response = requests.get(url)
        
        #logger.info(f"Server response status code: {response.status_code}")
        #logger.debug(f"Server response content: {response.text}")
        
        if response.status_code == 200:
            results = response.json()
            logger.info(f"Received inference results for user: {user_id}. Processing...")
            #logger.debug(f"Results content: {results}")
            for result in results:
                process_inference_result(user_id, result)
            logger.info(f"All files for user {user_id} have been processed.")
        elif response.status_code == 204:
            logger.info(f"No new inference results available for user {user_id}.")
        else:
            logger.error(f"Failed to get response from server for user {user_id}: {response.status_code}")
            logger.debug(f"Response content: {response.text}")
    
    except requests.RequestException as e:
        logger.error(f"Error occurred while receiving data from the server for user {user_id}: {str(e)}")
        logger.exception("Detailed error information:")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from server response for user {user_id}: {str(e)}")
        logger.exception("Detailed error information:")
    except Exception as e:
        logger.error(f"An unexpected error occurred for user {user_id}: {str(e)}")
        logger.exception("Detailed error information:")

def get_users_with_results():
    """Retrieve the list of users who have results available from the server."""
    try:
        url = f"{SERVER_URL}/get_users_with_results"
        response = requests.get(url)
        logger.info(f"Requesting list of users with results from server: {url}")
        
        if response.status_code == 200:
            users_with_results = response.json().get("users_with_results", [])
            logger.info(f"Users with results: {users_with_results}")
            return users_with_results
        else:
            logger.error(f"Failed to get users with results from server: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error occurred while fetching users with results: {str(e)}")
        logger.exception("Detailed error information:")
        return []

def main():
    """Main function to dynamically retrieve file results for all users with pending results."""
    users_with_results = get_users_with_results()
    
    if not users_with_results:
        logger.info("No users with results found.")
        return
    
    # Loop through each user ID and get their historical results
    for user_id in users_with_results:
        receive_inference_results(user_id)

if __name__ == "__main__":
    main()
