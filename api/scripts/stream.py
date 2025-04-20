import requests
url = "https://play-gate.254.radio/api/post/"

headers = {
	"Content-Type": "application/json"
}
payload = {
	"route": "content/api/stream/",
	"data": {
		"media": "e6665c33-6f0d-44dc-a7e3-76e1241ebedd",
	}}
response = requests.post(url, headers=headers, json=payload)
print("Status Code:", response.status_code)

try:
	print("Response:", response.json())
except ValueError:
	print("Non-JSON response:", response.text)