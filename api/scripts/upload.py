# import requests
# import json
#
url = "https://play-gate.254.radio/api/post/"
# file_path = "/Users/mac/Downloads/PLAYKE (2).mp3"
#
# payload = {
#     "route": "content/api/upload-media/",
#     "data": json.dumps({
#         "title": "Sample Title",
#         "artist": "12d21298-cadf-4da3-a13c-f78409f11bbd",
#         "album": "14072780-8afa-4375-8276-ce66e605bcfe",
#         "genre": "Hip-Hop",
#         "media_type": "audio",
#         "release_date": "2024-12-31",
#         "language": "English",
#         "tags": '["relax", "summer"]',
#         "is_explicit": 'false'
#     })
# }
#
# files = {
#     "file": open(file_path, "rb")
# }
#
# response = requests.post(url, data=payload, files=files)
# print("Status Code:", response.status_code)
# try:
#     print("Response:", response.json())
# except ValueError:
#     print("Non-JSON response:", response.text)
import requests

headers = {
    "Content-Type": "application/json"
}
payload = {
    "route":"content/api/stream/",
    "data": {
        "media": "bf4c5d5d-ec80-4cbe-bb1d-7bf902958350",
    }}
response = requests.post(url, headers=headers, json=payload)
print("Status Code:", response.status_code)

try:
    print("Response:", response.json())
except ValueError:
    print("Non-JSON response:", response.text)