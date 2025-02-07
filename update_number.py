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
        generator = pipeline("text-generation", model="openai-community/gpt2")
        generated = generator(COMMIT_MESSAGE_PROMPT, max_new_tokens=50, num_return_sequences=1, temperature=0.9, top_k=50, top_p=0.9, truncation=True)
        text = generated[0]["generated_text"]
        if "- " in text:
            return text.rsplit("- ", 1)[-1].strip()
        else:
            raise ValueError("Unexpected generated text")
    except Exception as e:
        logging.error(f"Error generating commit message: {e}")
        return f"Update number: {datetime.now().strftime('%Y-%m-%d')}"

# Run a subprocess command and handle errors
def run_subprocess(command):
    try:
        result = subprocess.run(["git", "push", "--no-verify"], check=True)

        logging.info(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred during subprocess execution: {e.stderr}")
        sys.exit(1)

# Commit the changes with a generated or default message
def git_commit():
    run_subprocess(["git", "add", os.path.join(REPO_DIR, NUMBER_FILE)])

    commit_message = generate_random_commit_message()
    run_subprocess(["git", "commit", "-m", commit_message])

# Push the changes to the remote repository
def git_push():
    result = run_subprocess(["git", "push"])
    if result.returncode == 0:
        logging.info("Changes pushed to GitHub successfully.")
    else:
        logging.error("Error pushing to GitHub.")
        sys.exit(1)

# Update cron or Task Scheduler with a random time
def update_task_scheduler():
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)

    if sys.platform.startswith("linux") or sys.platform == "darwin":
        # Linux/macOS Crontab Update
        cron_file = os.path.expanduser("~/.crontab")
        cron_job = f"{random_minute} {random_hour} * * * /usr/bin/python3 {os.path.join(REPO_DIR, 'update_number.py')}\n"
        try:
            with open(cron_file, "a") as crontab:
                crontab.write(cron_job)
            logging.info(f"Task scheduled on {random_hour}:{random_minute} via cron.")
        except Exception as e:
            logging.error(f"Failed to update crontab: {e}")
            sys.exit(1)
    elif sys.platform == "win32":
        # Windows Task Scheduler Update
        try:
            task_name = "AutoGitCommit"
            run_subprocess(["schtasks", "/create", "/tn", task_name, "/tr", f"python3 {os.path.join(REPO_DIR, 'update_number.py')}", "/sc", "daily", "/st", f"{random_hour:02}:{random_minute:02}"])
            logging.info(f"Task scheduled on {random_hour}:{random_minute} via Windows Task Scheduler.")
        except Exception as e:
            logging.error(f"Failed to update Windows Task Scheduler: {e}")
            sys.exit(1)

def main():
    set_working_directory()
    
    current_number = read_number()
    logging.info(f"Current number: {current_number}")
    
    new_number = current_number + 1
    write_number(new_number)

    git_commit()
    git_push()
    update_task_scheduler()

if __name__ == "__main__":
    main()
