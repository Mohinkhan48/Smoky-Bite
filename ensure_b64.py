import base64
try:
    with open('static/img/burger_category.jpg', 'rb') as f:
        data = f.read()
        b64 = base64.b64encode(data).decode('utf-8')
        with open('burger_b64.txt', 'w') as out:
            out.write(b64)
    print("Done")
except Exception as e:
    print(f"Error: {e}")
