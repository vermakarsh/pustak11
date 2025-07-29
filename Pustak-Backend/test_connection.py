import requests

# Test the test endpoint
url = "http://localhost:9001/api/test"

try:
    response = requests.get(url)
    print(f"Test API Status: {response.status_code}")
    print(f"Test API Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
