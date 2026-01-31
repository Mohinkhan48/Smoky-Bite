import os
import time

img_dir = r"c:\Users\User\OneDrive\Documents\Smoky Bites\static\img"
mapping = {
    "Burgerimage.png": "burger_v2.png",
    "Momos.png": "momos_v2.png",
    "Brost.png": "brost_v2.png",
    "Mocktails.png": "mocktails_v2.png",
    "Hotcrispy.png": "hotcrispy_v2.png",
    "Mediumcombo.png": "medium_v2.png",
    "Largecombo.png": "large_v2.png"
}

print(f"Starting rename in {img_dir}")
for old_name, new_name in mapping.items():
    old_path = os.path.join(img_dir, old_name)
    new_path = os.path.join(img_dir, new_name)
    
    # Try case-insensitive find
    if not os.path.exists(old_path):
        for f in os.listdir(img_dir):
            if f.lower() == old_name.lower():
                old_path = os.path.join(img_dir, f)
                break

    if os.path.exists(old_path):
        try:
            if os.path.exists(new_path):
                os.remove(new_path)
            os.rename(old_path, new_path)
            print(f"Success: {old_path} -> {new_name}")
        except Exception as e:
            print(f"Error renaming {old_name}: {e}")
    else:
        print(f"Not found: {old_name}")

print("Verification:")
print(os.listdir(img_dir))
