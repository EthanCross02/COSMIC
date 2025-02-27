"""
This script will be used to update the Raspberry Pi using crontab

THIS PROCESS IS CRUCIAL, PLEASE DO NOT EDIT WITHOUT TALKING TO ETHAN
"""

import subprocess
import os

def git_pull():
    # Set the working directory to the Git repo
    repo_path = "/home/EthansPi/COSMIC"
    os.chdir(repo_path)

    try:
    
        result = subprocess.run(["/usr/bin/git", "pull"], capture_output=True, text=True)
        print(result.stdout)
        print("This should have been successful")
        print(result.stderr)
    except:
        print("there was an error")

if __name__ == "__main__":
    git_pull()