import requests

with open("DAA/sales_data.csv", "rb") as f:
    response = requests.post("http://127.0.0.1:8000/", files={"dataset": f})
print(response.json())
