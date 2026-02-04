import os
from PIL import Image

def optimize_images(directory, max_width=800, quality=75):
    log_file = "optimization_log.txt"
    with open(log_file, "w") as log:
        if not os.path.exists(directory):
            log.write(f"Directory {directory} not found.\n")
            return

        files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        log.write(f"Found {len(files)} images to optimize in {directory}\n\n")

        for filename in files:
            filepath = os.path.join(directory, filename)
            original_size = os.path.getsize(filepath)
            
            try:
                with Image.open(filepath) as img:
                    # Force RGB if saving as JPG-like or if we want to save space
                    # But if we keep PNG, we keep transparency.
                    w, h = img.size
                    if w > max_width:
                        new_h = int(h * (max_width / w))
                        img = img.resize((max_width, new_h), Image.Resampling.LANCZOS)
                    
                    if filename.lower().endswith('.png'):
                        # PNG optimization
                        img.save(filepath, "PNG", optimize=True)
                    else:
                        img.save(filepath, "JPEG", quality=quality, optimize=True)
                    
                    new_size = os.path.getsize(filepath)
                    reduction = (original_size - new_size) / original_size * 100
                    log.write(f"Optimized {filename}: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB ({reduction:.1f}% smaller)\n")
                    
            except Exception as e:
                log.write(f"Error processing {filename}: {e}\n")

if __name__ == "__main__":
    img_dir = os.path.join('static', 'img')
    optimize_images(img_dir)
