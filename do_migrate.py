import subprocess
import os

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    return result

os.chdir(r"c:\Users\User\OneDrive\Documents\Smoky Bites")
python_exe = r"venv\Scripts\python.exe"

run_cmd(f"{python_exe} manage.py makemigrations orders")
run_cmd(f"{python_exe} manage.py migrate orders")
run_cmd(f"{python_exe} manage.py migrate")
