import subprocess
import os
import sys

def run_cmd(cmd):
    print(f"\n--- Running: {cmd} ---")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout: print("STDOUT:", res.stdout)
    if res.stderr: print("STDERR:", res.stderr)
    return res.returncode == 0

os.chdir(r"c:\Users\User\OneDrive\Documents\Smoky Bites")
python_exe = r"venv\Scripts\python.exe"

# 1. Migrate
if not run_cmd(f"{python_exe} manage.py migrate"):
    print("Migration FAILED")
    sys.exit(1)

# 2. Populate
if not run_cmd(f"{python_exe} master_populate.py"):
    print("Population FAILED")

# 3. Create User
user_cmd = f'{python_exe} -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username=\'admin\').exists() or User.objects.create_superuser(\'admin\', \'admin@example.com\', \'admin123\')"'
if not run_cmd(user_cmd):
    print("User creation FAILED")
