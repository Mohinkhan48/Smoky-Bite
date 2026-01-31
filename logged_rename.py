import os
import subprocess

log_file = r"c:\Users\User\OneDrive\Documents\Smoky Bites\rename_log.txt"
img_dir = r"c:\Users\User\OneDrive\Documents\Smoky Bites\static\img"

def log(msg):
    with open(log_file, "a") as f:
        f.write(msg + "\n")

if os.path.exists(log_file):
    os.remove(log_file)

log("Starting rename process...")

try:
    files = os.listdir(img_dir)
    log(f"Found files: {str(files)}")
    
    for f in files:
        if f.lower() != f:
            old_path = os.path.join(img_dir, f)
            new_path = os.path.join(img_dir, f.lower())
            temp_path = old_path + ".tmp"
            
            os.rename(old_path, temp_path)
            os.rename(temp_path, new_path)
            log(f"Renamed {f} -> {f.lower()}")
        else:
            log(f"Already lowercase: {f}")

    log("Staging in git...")
    # Add everything in the img dir
    subprocess.run(["git", "add", "static/img/*.png"], shell=True)
    
    # Check status
    res = subprocess.run(["git", "status"], capture_output=True, text=True)
    log("Git Status:\n" + res.stdout)

except Exception as e:
    log(f"Error: {str(e)}")

log("Done.")
