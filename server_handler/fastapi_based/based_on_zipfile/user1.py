import requests
import os
from datetime import datetime

# Remote server URL
REMOTE_SERVER_URL = "http://server ip:port from server_engine/receive_data"

# Get the absolute path of the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory where received ZIP files will be stored
RECEIVED_ZIP_DIR = os.path.join(SCRIPT_DIR, "received_zip")
os.makedirs(RECEIVED_ZIP_DIR, exist_ok=True)  # Ensure the directory exists

# Predefined user data
USER_DATA = {
    "user2":
        {
            "project_number": "PRJ-1080",
            "floor_numbers": "1",
            "images_name": os.path.join(SCRIPT_DIR, "original_img", "7.jpg"),
        }
}

def send_data(user_id, project_data, floor_number):
    try:
        # Check if the image file exists
        if not os.path.exists(project_data['images_name']):
            raise FileNotFoundError(f"Image file not found: {project_data['images_name']}")

        # Open the image file in binary mode
        with open(project_data['images_name'], "rb") as image_file:
            # Prepare the files and data to send in the POST request
            files = {
                "images": (os.path.basename(project_data['images_name']), image_file, "image/png")
            }
            payload = {
                "user_id": user_id,
                "project_number": project_data['project_number'],
                "floor_number": floor_number,
                "date": datetime.now().strftime("%Y-%m-%d")
            }

            # Send the POST request to the remote server with a timeout
            print(f"Sending data for {user_id}, Project: {project_data['project_number']}, Floor: {floor_number}...")
            response = requests.post(REMOTE_SERVER_URL, files=files, data=payload, timeout=120)

            # Handle the response from the server
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/zip':
                    # If the server sends back a ZIP file, save it
                    zip_filename = f"{user_id}.zip"  # Only the user_id in the zip file name
                    zip_filepath = os.path.join(RECEIVED_ZIP_DIR, zip_filename)

                    with open(zip_filepath, "wb") as f:
                        f.write(response.content)

                    print(f"Received ZIP file saved as {zip_filepath}")


                else:
                    # Unexpected content type, log and handle the error
                    print(f"Unexpected response content type: {content_type}. Expected a ZIP file.")
                    print(f"Response content: {response.text}")
            else:
                print(f"Failed to upload data for {user_id}, Project: {project_data['project_number']}, Floor: {floor_number}. Server responded with: {response.status_code} - {response.text}")
    
    except FileNotFoundError as e:
        print(f"File error for {user_id}, Project: {project_data['project_number']}, Floor: {floor_number}: {str(e)}")
    except requests.Timeout:
        print(f"Request timed out while sending data for {user_id}, Project: {project_data['project_number']}, Floor: {floor_number}")
    except Exception as e:
        print(f"An error occurred while sending data for {user_id}, Project: {project_data['project_number']}, Floor: {floor_number}: {str(e)}")

def main():
    # Print the current working directory and image paths for debugging
    print(f"Current working directory: {os.getcwd()}")
    for user_id, project_data in USER_DATA.items():
        print(user_id, project_data)        
        # Send data for each user (single project and floor)
        send_data(user_id, project_data, project_data['floor_numbers'])

if __name__ == "__main__":
    main()
