import os
import subprocess

img_dir = r"c:\Users\User\OneDrive\Documents\Smoky Bites\static\img"
files = os.listdir(img_dir)

for f in files:
    if f.lower() != f:
        old_path = os.path.join(img_dir, f)
        new_path = os.path.join(img_dir, f.lower())
        temp_path = old_path + ".tmp"
        
        # Rename to temp then to lower
        os.rename(old_path, temp_path)
        os.rename(temp_path, new_path)
        
        print(f"Renamed {f} -> {f.lower()}")
        
        # Git mv is the best way to tell git "this file changed case"
        # Since we already renamed on disk, we might need to git add
        subprocess.run(["git", "add", new_path])
        subprocess.run(["git", "rm", "--cached", old_path])

print("Renaming complete and staged.")
