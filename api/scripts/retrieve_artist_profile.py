

'retrieve_artist'

import requests

url = "https://play-gate.254.radio/api/post/"

payload = {
	"route": "content/api/retrieve_artist/",
	"data": {
		"artist":"22e698ad-e623-4e2f-a7a7-e72c3ead7c2a"
	}
}
response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
try:
	print("Response:", response.json())
except ValueError:
	print("Non-JSON response:", response.text)