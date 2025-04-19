import requests
import json
import base64

url = "https://play-gate.254.radio/api/proxy/"
headers = {
    "Authorization": "Bearer your_token",
    "Content-Type": "application/json"
}
file_path = "/Users/mac/Downloads/PLAYKE (2).mp3"
with open(file_path, "rb") as f:
    encoded_file = base64.b64encode(f.read()).decode("utf-8")
payload = {
    "target_system": {
        "name": "PlayContentService"
    },
    "route": {
        "path": "api/upload-media/",
        "method": "POST"
    },
    "data": {
        "title": "Sample Title",
        "artist": "12d21298-cadf-4da3-a13c-f78409f11bbd",
        "album": "14072780-8afa-4375-8276-ce66e605bcfe",
        "genre": "Hip-Hop",
        "media_type": "audio",
        "release_date": "2024-12-31",
        "language": "English",
        "tags": ["relax", "summer"],
        "is_explicit": False
    },
    "files": {
        "file": {
            "filename": "PLAYKE.mp3",
            "content_type": "audio/mpeg",
            "content": encoded_file
        }
    }
}
response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.status_code)
try:
    print(response.json())
except ValueError:
    print("Response is not valid JSON")
