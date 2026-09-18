import requests
from concurrent.futures import ThreadPoolExecutor


URL = "http://localhost:8000/api/v1/predict"

HEADERS = {
    "X-API-Key": "iris-api-2026"
}

DATA = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}


def send_request():
    response = requests.post(
        URL,
        headers=HEADERS,
        json=DATA
    )
    return response.status_code


with ThreadPoolExecutor(max_workers=50) as executor:
    results = list(
        executor.map(
            lambda _: send_request(),
            range(50)
        )
    )


print("Total requests:", len(results))
print("Successful requests:", results.count(200))
print("Failed requests:", len(results) - results.count(200))