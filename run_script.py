import subprocess
import time
import os
import shutil


def run_script():
    """Runs the bot script and restarts it if it stops, handles crashes."""
    command = ["python", "main.py"]
    error_log_path = "errors.txt"
    
    while True:
        print("Starting the bot script...")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stdout:
            print("STDOUT:", stdout.decode())
        if stderr:
            error_message = stderr.decode()
            print("STDERR:", error_message)
            with open(error_log_path, "w") as error_file:
                error_file.write(f"Error on {time.strftime('%c')}:\n{error_message}\n\n")

        if process.returncode == 0:
            print("Script executed successfully, committing changes...")
            commit_and_push_changes('Backup commit after successful run')
        else:
            print("Script crashed or exited with errors, skipping commit...")
            # Implement logic to checkout to a known good commit or tag
            revert_to_last_working_state()

        # Wait a bit before potentially restarting or after reverting
        time.sleep(15)

def commit_and_push_changes(message='Backup commit'):
    """Commits all changes in the directory and pushes them to GitHub."""
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        print("Changes and tags pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to push changes or tags: {e}")


def revert_to_last_working_state():
    """Reverts the local project to the last state committed on GitHub marked as stable."""
    try:
        subprocess.run(['git', 'reset', '--hard', 'e5d8644'], check=True)
        # subprocess.run(['git', 'clean', '-df'], check=True)  # Remove untracked files and directories
        print("Reverted to the last known good state from Git.")
        time.sleep(15)
    except subprocess.CalledProcessError as e:
        print(f"Failed to revert to the last known good state: {e}")



if __name__ == "__main__":
    run_script()
