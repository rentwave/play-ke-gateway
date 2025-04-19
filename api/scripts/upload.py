import requests
url = "https://play-gate.254.radio/api/proxy/"

file_path = "/Users/mac/Downloads/PLAYKE (2).mp3"
payload = {
    "route":"content/api/upload-media/",
    "data": {
        "title": "Sample Title",
        "artist": "12d21298-cadf-4da3-a13c-f78409f11bbd",
        "album": "14072780-8afa-4375-8276-ce66e605bcfe",
        "genre": "Hip-Hop",
        "media_type": "audio",
        "release_date": "2024-12-31",
        "language": "English",
        "tags": '["relax", "summer"]',
        "is_explicit": 'false'
    }
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

