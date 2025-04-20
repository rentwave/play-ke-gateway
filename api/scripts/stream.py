import requests

headers = {
	"Content-Type": "application/json"
}
payload = {
	"route": "content/api/stream/",
	"data": {
		"media": "bf4c5d5d-ec80-4cbe-bb1d-7bf902958350",
	}}
response = requests.post(url, headers=headers, json=payload)
print("Status Code:", response.status_code)

try:
	print("Response:", response.json())
except ValueError:
	print("Non-JSON response:", response.text)