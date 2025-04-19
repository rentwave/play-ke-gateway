import requests

url = "https://play-gate.254.radio/api/proxy/"
headers = {
    "Authorization": "Bearer a19496f4fdfcbc89f9ddfab7f5f6614d7a87d304b5575fd6779fbb6e4f66680116dc26f5e7552abe3e295f7034821b5e3efa"
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
