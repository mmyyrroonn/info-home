import requests
import json

url = "https://info.myron-moshui.online/twitter/queryRelatedTwitter"

payload="{\r\n    \"query_text\": \"空投,融资,币安,作业,撸毛\",\r\n    \"limit\": 100\r\n}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload.encode('utf-8'))

res = response.json()['data']
texts = []
for item in res:
    texts.append(item['text'])
print(texts)