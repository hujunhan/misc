"""
A script to check all git repositories in a directory for uncommitted changes. 
"""
import os
import subprocess
import sys
import time
import datetime
import re
import glob

# Get the path to the folder containing all the git repositories
root_path = "/Users/hu/code"

# iterate over all the folders in the root_path
# just iterate over the first level of folders
for dir in os.listdir(root_path):
    # get the path to the current folder
    path = os.path.join(root_path, dir)
    # check if the current folder is a git repository
    if os.path.exists(os.path.join(path, ".git")):
        # change the current working directory to the current folder
        os.chdir(path)
        # run the git status command and capture the output
        output = subprocess.run(
            ["git", "status"], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
        # check if the output contains the string "nothing to commit"
        if "nothing to commit" in output:
            # print(f'{path} is clean')
            pass
        else:
            print(f"{path} is dirty")
            # print(output)
            print()
