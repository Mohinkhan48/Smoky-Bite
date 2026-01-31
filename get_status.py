import subprocess
import os

try:
    with open("git_output.txt", "w") as f:
        subprocess.run(["git", "status"], stdout=f, stderr=f, timeout=30)
except Exception as e:
    with open("git_output.txt", "w") as f:
        f.write(f"Error: {str(e)}")
