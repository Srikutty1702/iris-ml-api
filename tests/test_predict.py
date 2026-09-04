def test_predict_valid_input(client):
    response = client.post(
        "/api/v1/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "confidence" in data
    assert "request_id" in data

    assert data["prediction"] in [0, 1, 2]
    assert 0 <= data["confidence"] <= 1

def test_predict_missing_field(client):
    response = client.post(
        "/api/v1/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4
        }
    )

    assert response.status_code == 422

def test_predict_invalid_value(client):
    response = client.post(
        "/api/v1/predict",
        json={
            "sepal_length": -1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 422

def test_predict_batch_oversized(client):
    inputs = [
        {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
        for _ in range(101)
    ]

    response = client.post(
        "/api/v1/predict-batch",
        json={"inputs": inputs}
    )

    assert response.status_code == 400