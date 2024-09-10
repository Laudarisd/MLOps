import threading
import os

def run_script(script_name):
    """
    Function to run a script using os.system.
    """
    os.system(f"python3 {script_name}")

def main():
    # List of user scripts to run in parallel
    #scripts = ["user1.py", "user2.py", "user3.py"]
    scripts = ["user2.py"]
    # Create and start a thread for each script
    threads = []
    for script in scripts:
        thread = threading.Thread(target=run_script, args=(script,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All scripts have finished execution.")

if __name__ == "__main__":
    main()
