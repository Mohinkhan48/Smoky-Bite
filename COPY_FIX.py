import shutil
import os

img_dir = r"c:\Users\User\OneDrive\Documents\Smoky Bites\static\img"
mapping = {
    "Burgerimage.png": "burger_final.png",
    "Momos.png": "momos_final.png",
    "Brost.png": "brost_final.png",
    "Mocktails.png": "mocktails_final.png",
    "Hotcrispy.png": "hotcrispy_final.png",
    "Mediumcombo.png": "medium_final.png",
    "Largecombo.png": "large_final.png"
}

print(f"Copying files in {img_dir}")
for old_name, new_name in mapping.items():
    old_path = os.path.join(img_dir, old_name)
    new_path = os.path.join(img_dir, new_name)
    
    # Check if old path exists (case-sensitive)
    if os.path.exists(old_path):
        try:
            shutil.copy2(old_path, new_path)
            print(f"SUCCESS: Copied {old_name} to {new_name}")
        except Exception as e:
            print(f"FAIL: {old_name} -> {new_name}: {e}")
    else:
        print(f"NOT FOUND: {old_name}")

print("Current files:")
print(os.listdir(img_dir))
