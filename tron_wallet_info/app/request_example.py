import requests
import json

url = "http://127.0.0.1:8000/wallet-info/"
headers = {"Content-Type": "application/json"}
data = {"address": "TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7"}

response = requests.post(url, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())