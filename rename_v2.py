import os

img_dir = r"c:\Users\User\OneDrive\Documents\Smoky Bites\static\img"
mapping = {
    "Momos.png": "momos_v2.png",
    "Burgerimage.png": "burger_v2.png",
    "Brost.png": "brost_v2.png",
    "Mocktails.png": "mocktails_v2.png",
    "Hotcrispy.png": "hotcrispy_v2.png",
    "Mediumcombo.png": "medium_v2.png",
    "Largecombo.png": "large_v2.png"
}

for old, new in mapping.items():
    old_path = os.path.join(img_dir, old)
    new_path = os.path.join(img_dir, new)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed {old} to {new}")
    else:
        # Maybe it's already lowercase on disk but not in git?
        old_path_lower = os.path.join(img_dir, old.lower())
        if os.path.exists(old_path_lower):
            os.rename(old_path_lower, new_path)
            print(f"Renamed {old.lower()} to {new}")
