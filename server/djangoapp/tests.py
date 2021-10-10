import requests
import json

url = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/7eed226c81af75dae086a851aa8986b232fbb65a5f0a0483731fc5046f29267e/api/review"

payload = json.dumps({
  "doc": {
    "id": 107
  }
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
