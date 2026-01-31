import os

img_dir = r"c:\Users\User\OneDrive\Documents\Smoky Bites\static\img"
mapping = {
    "Brost.png": "brost_v2.png",
    "Burgerimage.png": "burger_v2.png",
    "Hotcrispy.png": "hotcrispy_v2.png",
    "Largecombo.png": "large_v2.png",
    "Mediumcombo.png": "medium_v2.png",
    "Mocktails.png": "mocktails_v2.png",
    "Momos.png": "momos_v2.png"
}

print(f"Checking directory: {img_dir}")
files_on_disk = os.listdir(img_dir)
print(f"Files found: {files_on_disk}")

for old, new in mapping.items():
    old_path = os.path.join(img_dir, old)
    new_path = os.path.join(img_dir, new)
    if os.path.exists(old_path):
        try:
            os.rename(old_path, new_path)
            print(f"SUCCESS: Renamed {old} -> {new}")
        except Exception as e:
            print(f"ERROR: Could not rename {old}: {e}")
    else:
        print(f"SKIP: {old} not found")

print("Cleanup: Checking for lowercase variants...")
for f in os.listdir(img_dir):
    if f.lower() in [k.lower() for k in mapping.keys()]:
        # If it's something like burgerimage.png instead of Burgerimage.png
        current_path = os.path.join(img_dir, f)
        for _, final_name in mapping.items():
            if f.lower().split('.')[0] in final_name:
                 # This is a bit fuzzy but let's just use the direct mapping for now
                 pass
