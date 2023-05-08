import requests

#response = requests.post('http://127.0.0.1:5000/ad/', json={'title': 'Title Ad', 'description': 'Description Ad', 'user': '1'})
#response = requests.get('http://127.0.0.1:5000/ad/1/')
response = requests.delete('http://127.0.0.1:5000/ad/1/')

print(response.status_code)
print(response.text)
