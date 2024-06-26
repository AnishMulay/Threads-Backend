import requests

BASE = "http://localhost:5000"

response = requests.post(BASE + "/item-resource", json={
    "name": "bunty",
    "description": "Red T Shirt"
})

print(response.json())
