import json

import requests

url = "https://play-gate.254.radio/api/post/"

headers = {
	"Content-Type": "application/json"
}

payload = {
	"route": "auth/user_management/auth/authenticate/",
	"data": {
		"phone_number": "0797270900",
		"email": "",
		"password": "123456"
 }
}


response = requests.post(url, json=payload, headers=headers)
print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except ValueError:
    print("Non-JSON response:", response.text)