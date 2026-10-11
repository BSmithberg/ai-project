import requests

url = "http://127.0.0.1:5000/chat"

payload = {
    "question": "Security"
}

response = requests.post(url, json=payload)

print("Status:", response.statuscode)
print("Response:", response.json())