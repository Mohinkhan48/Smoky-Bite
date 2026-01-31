import base64
import os

try:
    path = 'static/img/download.jpg'
    if not os.path.exists(path):
        print(f"File not found: {path}")
        exit(1)
        
    with open(path, 'rb') as f:
        data = f.read()
        b64 = base64.b64encode(data).decode('utf-8')
        with open('b64_output.txt', 'w') as out:
            out.write(b64)
    print("Done")
except Exception as e:
    print(f"Error: {e}")
