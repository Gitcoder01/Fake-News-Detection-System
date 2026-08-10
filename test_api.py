import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "text": "The president signed a new economic policy today."
}

response = requests.post(url, json=data)

print(response.json())