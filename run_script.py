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
            commit_and_push_changes('Backup commit after successful run')
        else:
            print("Script crashed or exited with errors, attempting to revert from GitHub...")
            revert_to_last_working_state()

        # Wait a bit before potentially restarting or after reverting
        time.sleep(3)

def commit_and_push_changes(message='Backup commit'):
    """Commits all changes in the directory and pushes them to GitHub."""
    try:
        # Add all changed files to the staging area
        subprocess.run(['git', 'add', '.'], check=True)

        # Commit the changes
        subprocess.run(['git', 'commit', '-m', message], check=True)

        # Push the changes to GitHub
        subprocess.run(['git', 'push'], check=True)

        print("Changes pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to push changes: {e}")

def revert_to_last_working_state():
    """Reverts the local project to the last state committed on GitHub."""
    try:
        # Reset local changes
        subprocess.run(['git', 'reset', '--hard'], check=True)

        # Pull the latest changes from GitHub
        subprocess.run(['git', 'pull'], check=True)

        print("Reverted to the last working state from GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to revert to the last working state: {e}")


if __name__ == "__main__":
    run_script()
