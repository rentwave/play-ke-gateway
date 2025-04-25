import requests
import json
url = "https://play-gate.254.radio/api/post/"
file_path = "/Users/mac/Downloads/cheza.mp3"

payload = {
    "route": "content/api/upload/",
    "title": "tath",
    "artist": "d49b14f04a884d849b206d48de3b0135",
    "album": "14072780-8afa-4375-8276-ce66e605bcfe",
    "genre": "Hip-Hop",
    "media_type": "audio",
    "release_date": "2024-12-31",
    "language": "English",
    "is_explicit": 'no',
"file": open(file_path, "rb")
}

files = {
    "file": open(file_path, "rb")
}

response = requests.post(url, data=payload, files=files)
print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except ValueError:
    print("Non-JSON response:", response.text)
 