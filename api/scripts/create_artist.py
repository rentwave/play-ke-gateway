import requests
import json
url = "https://play-gate.254.radio/api/post/"
file_path = "/Users/mac/Downloads/budyxcvivmfgfolmb61fcfafd99824.jpg"


payload = {
	"route": "content/api/create-artist/",
	"data": json.dumps({
	  "name": "John Doe",
	  "stage_name": "JD Blaze",
	  "bio": "An Afrobeat artist based in Nairobi.",
	  "origin_country": "Kenya",
	  "user_id": "123",
	  "debut_year": "2020"
	})
}

files = {
    "file": open(file_path, "rb")
}
print(files)
response = requests.post(url, data=payload, files=files)
print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except ValueError:
    print("Non-JSON response:", response.text)