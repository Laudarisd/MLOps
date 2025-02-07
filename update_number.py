#!/usr/bin/env python3
import os
import sys
import random
import subprocess
from datetime import datetime

# Force the script to always run from the correct repo
script_dir = r"D:\workspace\personal\git_management\MLOps"
os.chdir(script_dir)

# Debugging
print(f"Script directory forced to: {script_dir}")
print(f"After changing, Current working directory: {os.getcwd()}")

# Debugging: Print the directories
print(f"Script directory: {script_dir}")
print(f"Before changing, Current working directory: {os.getcwd()}")

# Change to the script directory
os.chdir(script_dir)

# Debugging: Verify the directory change
print(f"After changing, Current working directory: {os.getcwd()}")


def read_number():
    with open(os.path.join(script_dir, "number.txt"), "r") as f:
        return int(f.read().strip())


def write_number(num):
    with open(os.path.join(script_dir, "number.txt"), "w") as f:
        f.write(str(num))


def generate_random_commit_message():
    from transformers import pipeline

    generator = pipeline(
        "text-generation",
        model="openai-community/gpt2",
    )
    prompt = """
        Generate a Git commit message following the Conventional Commits standard. The message should include a type, an optional scope, and a subject.Please keep it short. Here are some examples:

        - feat(auth): add user authentication module
        - fix(api): resolve null pointer exception in user endpoint
        - docs(readme): update installation instructions
        - chore(deps): upgrade lodash to version 4.17.21
        - refactor(utils): simplify date formatting logic

        Now, generate a new commit message:
    """
    generated = generator(
        prompt,
        max_new_tokens=50,
        num_return_sequences=1,
        temperature=0.9,
        top_k=50,
        top_p=0.9,
        truncation=True,
    )
    text = generated[0]["generated_text"]

    if "- " in text:
        return text.rsplit("- ", 1)[-1].strip()
    else:
        raise ValueError(f"Unexpected generated text {text}")


def git_commit():
    subprocess.run(["git", "add", os.path.join(script_dir, "number.txt")], check=True)

    if "FANCY_JOB_USE_LLM" in os.environ:
        commit_message = generate_random_commit_message()
    else:
        date = datetime.now().strftime("%Y-%m-%d")
        commit_message = f"Update number: {date}"

    subprocess.run(["git", "commit", "-m", commit_message], check=True)


def git_push():
    result = subprocess.run(["git", "push"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)


def update_cron_with_random_time():
    """Schedules the script using crontab on Linux/macOS or Task Scheduler on Windows."""

    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)

    if sys.platform.startswith("linux") or sys.platform == "darwin":
        # **Linux/macOS Crontab Update**
        cron_file = os.path.join(script_dir, "current_cron.txt")

        new_cron_command = f"{random_minute} {random_hour} * * * cd {script_dir} && python3 {os.path.join(script_dir, 'update_number.py')}\n"

        os.system(f"crontab -l > {cron_file} 2>/dev/null || true")

        with open(cron_file, "r") as file:
            lines = file.readlines()

        with open(cron_file, "w") as file:
            for line in lines:
                if "update_number.py" not in line:
                    file.write(line)
            file.write(new_cron_command)

        os.system(f"crontab {cron_file}")
        os.remove(cron_file)

        print(f"[Linux/macOS] Cron job updated to run at {random_hour}:{random_minute}.")

    elif sys.platform == "win32":
        # **Windows Task Scheduler Update**
        task_name = "AutoGitCommit"
        script_path = os.path.abspath(__file__)

        print(f"[Windows] Scheduling task at {random_hour:02}:{random_minute:02}")

        # Remove the old scheduled task if it exists
        subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True)

        # Create a new scheduled task
        command = f'schtasks /create /tn "{task_name}" /tr "python {script_path}" /sc daily /st {random_hour:02}:{random_minute:02}"'
        subprocess.run(command, shell=True)

        print(f"[Windows] Task scheduled to run daily at {random_hour:02}:{random_minute:02}.")
    else:
        print("Unsupported OS: Cannot schedule tasks.")



def main():
    try:
        current_number = read_number()
        new_number = current_number + 1
        write_number(new_number)
        git_commit()
        git_push()
        update_cron_with_random_time()
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
