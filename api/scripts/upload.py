import requests
import json
url = "https://play-gate.254.radio/api/post/"
file_path = "/Users/mac/Downloads/Teslah - Rum in my cup.mp4"

payload = {
    "route": "content/api/upload/",
    "data": json.dumps({
        "title": "Kichele",
        "artist": "12d21298-cadf-4da3-a13c-f78409f11bbd",
        "album": "14072780-8afa-4375-8276-ce66e605bcfe",
        "genre": "Hip-Hop",
        "media_type": "video",
        "release_date": "2024-12-31",
        "language": "English",
        "is_explicit": 'no'
    })
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
 