#!/usr/bin/env python3
import os
import sys
import random
import subprocess
import logging
from datetime import datetime
from transformers import pipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
REPO_DIR = r"D:\workspace\personal\git_management\MLOps"
NUMBER_FILE = "number.txt"
GIT_REPO_URL = "https://github.com/Laudarisd/MLOps.git"
COMMIT_MESSAGE_PROMPT = """
    Generate a Git commit message following the Conventional Commits standard. The message should include a type, an optional scope, and a subject. Please keep it short. Here are some examples:
    - feat(auth): add user authentication module
    - fix(api): resolve null pointer exception in user endpoint
    - docs(readme): update installation instructions
    - chore(deps): upgrade lodash to version 4.17.21
    - refactor(utils): simplify date formatting logic

    Now, generate a new commit message:
"""

# Force the script to always run from the correct repo
def set_working_directory():
    try:
        os.chdir(REPO_DIR)
        logging.info(f"Working directory set to: {REPO_DIR}")
    except Exception as e:
        logging.error(f"Failed to change directory: {e}")
        sys.exit(1)

# Read the number from the file
def read_number():
    try:
        with open(os.path.join(REPO_DIR, NUMBER_FILE), "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        logging.error(f"{NUMBER_FILE} not found. Please ensure the file exists.")
        sys.exit(1)
    except ValueError:
        logging.error("Invalid value in number.txt, expected an integer.")
        sys.exit(1)

# Write the updated number to the file
def write_number(num):
    try:
        with open(os.path.join(REPO_DIR, NUMBER_FILE), "w") as f:
            f.write(str(num))
        logging.info(f"Number updated to: {num}")
    except Exception as e:
        logging.error(f"Failed to write to {NUMBER_FILE}: {e}")
        sys.exit(1)

# Generate a random commit message using LLM
def generate_random_commit_message():
    try:
        # Initialize LLM pipeline
        generator = pipeline("text-generation", model="openai-community/gpt2")

        # Generate the commit message
        generated = generator(COMMIT_MESSAGE_PROMPT, max_new_tokens=50, num_return_sequences=1, temperature=0.9, top_k=50, top_p=0.9, truncation=True)
        text = generated[0]["generated_text"]

        # Check if a valid commit message is generated
        if "- " in text:
            # Extract the commit message by splitting the generated text
            commit_message = text.rsplit("- ", 1)[-1].strip()
            logging.info(f"Generated commit message: {commit_message}")
            return commit_message
        else:
            # Fallback if the generated message isn't valid
            logging.warning("Generated message is invalid, using default commit message.")
            return f"Update number: {datetime.now().strftime('%Y-%m-%d')}"
    except Exception as e:
        logging.error(f"Error generating commit message: {e}")
        # Fallback if an error occurs
        return f"Update number: {datetime.now().strftime('%Y-%m-%d')}"

# Run a subprocess command and handle errors
def run_subprocess(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info(f"Command output: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred during subprocess execution: {e.stderr}")
        sys.exit(1)

# Perform the git commit and push
def git_commit_and_push():
    # Prepare the git commit command
    subprocess.run(["git", "add", os.path.join(REPO_DIR, NUMBER_FILE)], check=True)

    # Decide commit message based on the LLM environment variable
    if "FANCY_JOB_USE_LLM" in os.environ and os.environ["FANCY_JOB_USE_LLM"].lower() == "true":
        commit_message = generate_random_commit_message()
    else:
        commit_message = f"Update number: {datetime.now().strftime('%Y-%m-%d')}"

    # Commit with the generated message
    subprocess.run(["git", "commit", "-m", commit_message], check=True)

    # Push the changes to GitHub
    result = run_subprocess(["git", "push", "--no-verify"])

    if result.returncode == 0:
        logging.info("Changes pushed to GitHub successfully.")
    else:
        logging.error("Error pushing to GitHub.")
        sys.exit(1)

# Schedule the task on Windows
def schedule_task():
    try:
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        schedule_command = f"SchTasks /Create /SC DAILY /TN AutoGitCommit /TR 'python {os.path.abspath(__file__)}' /ST {random_hour:02d}:{random_minute:02d}"

        # Schedule task with Windows Task Scheduler
        result = subprocess.run(schedule_command, capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            logging.info(f"Task scheduled at {random_hour:02d}:{random_minute:02d} via Windows Task Scheduler.")
        else:
            logging.error(f"Error scheduling task: {result.stderr}")
    except Exception as e:
        logging.error(f"Error scheduling task: {e}")
        sys.exit(1)

if __name__ == "__main__":
    set_working_directory()

    # Read the current number, increment it, and write it back
    current_number = read_number()
    logging.info(f"Current number: {current_number}")
    write_number(current_number + 1)

    # Commit and push the changes to GitHub
    git_commit_and_push()

    # Schedule the task for the next run
    schedule_task()
