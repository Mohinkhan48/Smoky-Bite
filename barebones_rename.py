import os

img_dir = r"c:\Users\User\OneDrive\Documents\Smoky Bites\static\img"
try:
    files = os.listdir(img_dir)
    for f in files:
        if f.lower() != f:
            old_path = os.path.join(img_dir, f)
            new_path = os.path.join(img_dir, f.lower())
            temp_path = old_path + ".tmp"
            os.rename(old_path, temp_path)
            os.rename(temp_path, new_path)
except:
    pass
