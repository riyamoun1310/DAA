import requests

with open("dummy.csv", "rb") as df, open("test_questions.txt", "rb") as qf:
    files = {"dataset": df, "questions": qf}
    response = requests.post("http://127.0.0.1:8000/api", files=files)
    try:
        print(response.json())
    except Exception:
        print(response.text)
