import requests
import random
from datetime import datetime
import os

# Remote server URL
REMOTE_SERVER_URL = "http://your ip/receive_data"

# Get the absolute path of the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Predefined user data
USER_DATA = {
    "user8": [
        {
            "project_number": "PRJ-1087",
            "floor_numbers": ["23"],
            "images_name": os.path.join(SCRIPT_DIR, "original_img", "1.png"),
        },
        {
            "project_number": "PRJ-1009",
            "floor_numbers": ["30"],
            "images_name": os.path.join(SCRIPT_DIR, "original_img", "4.png"),
        }
    ],
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

            # Send the POST request to the remote server
            print(f"Sending data for {user_id}, Project: {project_data['project_number']}, Floor: {floor_number}...")
            response = requests.post(REMOTE_SERVER_URL, files=files, data=payload)

            # Handle the response from the server
            if response.status_code == 200:
                print(f"Successfully uploaded data for {user_id}, Project: {project_data['project_number']}, Floor: {floor_number} to the remote server.")
                print(f"Server response: {response.json()}")
            else:
                print(f"Failed to upload data for {user_id}, Project: {project_data['project_number']}, Floor: {floor_number}. Server responded with: {response.status_code} - {response.text}")
    
    except FileNotFoundError as e:
        print(f"File error for {user_id}, Project: {project_data['project_number']}, Floor: {floor_number}: {str(e)}")
    except Exception as e:
        print(f"An error occurred while sending data for {user_id}, Project: {project_data['project_number']}, Floor: {floor_number}: {str(e)}")

def main():
    # Print the current working directory and image paths for debugging
    print(f"Current working directory: {os.getcwd()}")
    for user, projects in USER_DATA.items():
        for project in projects:
            print(f"{user} - Project: {project['project_number']}, Floors: {project['floor_numbers']}, Image path: {project['images_name']}")
            print(f"Image exists: {os.path.exists(project['images_name'])}")

            #Iterate over each floor number in the current project
            for floor_number in project['floor_numbers']:
                send_data(user, project, floor_number)

if __name__ == "__main__":
    main()