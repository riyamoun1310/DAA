import requests

with open("test_questions.txt", "rb") as qf:
    files = {"questions": qf}
    response = requests.post("http://127.0.0.1:8000/api", files=files)
    print(response.json())
