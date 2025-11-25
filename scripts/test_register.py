import requests
import json

def test_register():
    url = "http://127.0.0.1:8000/register/"
    data = {
        "username": "testuser",
        "user_password": "testpassword"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    test_register()
