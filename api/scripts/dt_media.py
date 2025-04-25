import requests
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer NmM3ODRiMDkwOGE4ZWFlNDI1ZGRiYThhZmY4NGQ3"
filePath = "/Users/mac/Downloads/__CAROLINESTATEMENT.pdf"
url = 'https://api.spinmobile.co/api/file/upload/'
files = {'document': open(filePath, 'rb')}

values = {
    'document_type': 'BANK',
      'organization_code': 'LP',
      'decrypter': '',
      'bank_code': 'NBK',
      'sender': ''
}
resp = requests.post(url, files=files, data=values, headers=headers)
print(resp.json())

