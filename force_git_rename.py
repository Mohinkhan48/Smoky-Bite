import os
import subprocess

img_dir = r"c:\Users\User\OneDrive\Documents\Smoky Bites\static\img"
os.chdir(img_dir)

files = [
    "Brost.png", "Burgerimage.png", "Hotcrispy.png", 
    "Largecombo.png", "Mediumcombo.png", "Mocktails.png", "Momos.png"
]

for f in files:
    try:
        lower_f = f.lower()
        temp_f = lower_f + ".tmp"
        
        # Step 1: mv to temp
        subprocess.run(["git", "mv", f, temp_f], check=True)
        # Step 2: mv to lower
        subprocess.run(["git", "mv", temp_f, lower_f], check=True)
        print(f"Successfully renamed {f} to {lower_f}")
    except Exception as e:
        print(f"Failed to rename {f}: {e}")

subprocess.run(["git", "add", "."], check=True)
print("Finished.")
