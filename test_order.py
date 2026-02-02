import requests
import json

url = "http://127.0.0.1:8000/place_order/"
data = {
    "items": [{"id": 1, "quantity": 1}], # This assumes an item with ID 1 exists
    "payment_method": "UPI",
    "customer_name": "Test User",
    "customer_number": "1234567890"
}

try:
    # We skip CSRF for this test script as it's an external tool
    # But the view is @csrf_exempt so it should be fine.
    response = requests.post(url, json=data, timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
