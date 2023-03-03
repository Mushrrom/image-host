import requests
from requests.structures import CaseInsensitiveDict

url = "http://127.0.0.1:5000/createaccount"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = '{"username": "asd"}'


resp = requests.post(url, headers=headers, data=data)

print(resp.status_code)
