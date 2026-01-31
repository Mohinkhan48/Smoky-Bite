import subprocess
import os

os.chdir(r"c:\Users\User\OneDrive\Documents\Smoky Bites")
python_exe = r"venv\Scripts\python.exe"

with open("setup_debug.log", "w") as f:
    f.write("Starting setup...\n")
    try:
        res = subprocess.run([python_exe, "manage.py", "migrate"], capture_output=True, text=True)
        f.write("--- MIGRATE STDOUT ---\n")
        f.write(res.stdout)
        f.write("--- MIGRATE STDERR ---\n")
        f.write(res.stderr)
        
        res = subprocess.run([python_exe, "master_populate.py"], capture_output=True, text=True)
        f.write("--- POPULATE STDOUT ---\n")
        f.write(res.stdout)
        f.write("--- POPULATE STDERR ---\n")
        f.write(res.stderr)
        
        # Superuser
        cmd = "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
        res = subprocess.run([python_exe, "manage.py", "shell", "-c", cmd], capture_output=True, text=True)
        f.write("--- USER STDOUT ---\n")
        f.write(res.stdout)
        f.write("--- USER STDERR ---\n")
        f.write(res.stderr)
        
    except Exception as e:
        f.write(f"FATAL ERROR: {str(e)}\n")

print("Setup script finished.")
