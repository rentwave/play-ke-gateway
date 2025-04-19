import requests

url = "https://play-gate.254.radio/api/proxy/"
headers = {
    "Authorization": "Bearer cc753f73499c23d2ec1c1db3d32ea6a282fb96d6c5d12073371f57cc8b9e025212cf6959b8cf0451fb4e610f8d93c4214ecf"
}

payload = {
    "target_system[name]": "play-content",
    "route[path]": "/api/media/upload/",
    "route[method]": "POST",
    "data[title]": "Sample Title",
    "data[artist]": "12d21298-cadf-4da3-a13c-f78409f11bbd",
    "data[album]": "14072780-8afa-4375-8276-ce66e605bcfe",
    "data[genre]": "Hip-Hop",
    "data[media_type]": "audio",
    "data[release_date]": "2024-12-31",
    "data[language]": "English",
    "data[tags]": '["relax", "summer"]',
    "data[is_explicit]": "false",
}
files = {
    "files[file]": open('/Users/mac/Downloads/PLAYKE (2).mp3', 'rb')
}

response = requests.post(url, headers=headers, data=payload, files=files)

print(response.status_code)
try:
    print(response.json())
except ValueError:
    print("Response content is not in JSON format.")
