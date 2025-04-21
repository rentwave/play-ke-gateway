import requests

url = "https://play-gate.254.radio/api/post/"
data = {
	"draw": 1,
	"columns": [
		{
			"data": "id",
			"name": "",
			"orderable": True,
			"search": {
				"regex": False,
				"value": ""
			},
			"searchable": True
		},
		{
			"data": "media_type",
			"name": "",
			"orderable": True,
			"search": {
				"regex": False,
				"value": ""
			},
			"searchable": True
		},
		{
			"data": "state__name",
			"name": "",
			"orderable": True,
			"search": {
				"regex": False,
				"value": ""
			},
			"searchable": True
		},
		{
			"data": "date_created",
			"name": "",
			"orderable": True,
			"search": {
				"regex": False,
				"value": ""
			},
			"searchable": True
		}
	
	],
	"state_filter": "",
	"order": [
		{
			"column": 7,
			"dir": "DESC"
		}
	],
	"start": 0,
	"length": 10,
	"search": {
		"value": "",
		"regex": False
	},
}
headers = {
	"Content-Type": "application/json"
}
payload = {
	"route": "content/api/dt_media/",
	"data": data
}

response = requests.post(url, headers=headers, json=payload)
print("Status Code:", response.status_code)

try:
	print("Response:", response.json())
except ValueError:
	print("Non-JSON response:", response.text)