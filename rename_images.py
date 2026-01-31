import os

img_dir = r"c:\Users\User\OneDrive\Documents\Smoky Bites\static\img"
files = os.listdir(img_dir)
for f in files:
    old_path = os.path.join(img_dir, f)
    new_path = os.path.join(img_dir, f.lower())
    if old_path != new_path:
        # On Windows, rename(A, a) might not do anything if it's case-insensitive
        # So we use a temporary name
        temp_path = old_path + ".tmp"
        os.rename(old_path, temp_path)
        os.rename(temp_path, new_path)
        print(f"Renamed {f} to {f.lower()}")
