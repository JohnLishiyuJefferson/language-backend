import requests

url = "http://localhost:8000/process"
data = {"text": "hello world"}
response = requests.post(url, json=data)

print(response.json())  # 输出: {'processed_text': 'HELLO WORLD'}
