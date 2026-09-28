import requests


url = "http://127.0.0.1:5000/predict"


data = {
    "text": """
    The United States government announced new measures on Wednesday
    to support economic growth and strengthen cooperation with its allies.
    Officials said the measures would take effect later this year.
    """
}


response = requests.post(url, json=data)


print("Status Code:", response.status_code)
print("Response:")

try:
    print(response.json())

except ValueError:
    print(response.text)
