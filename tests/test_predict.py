def test_predict_valid_input(client):
    response = client.post(
    "/api/v1/predict",
    headers={"X-API-Key": "iris-api-2026"},
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
        headers={"X-API-Key": "iris-api-2026"},
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
        headers={"X-API-Key": "iris-api-2026"},
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
        headers={"X-API-Key": "iris-api-2026"},
        json={"inputs": inputs}
    )

    assert response.status_code == 400

def test_v1_v2_response_shapes(client):
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    v1_response = client.post(
        "/api/v1/predict",
        headers={"X-API-Key": "iris-api-2026"},
        json=payload
    )

    v2_response = client.post(
        "/api/v2/predict",
        headers={"X-API-Key": "iris-api-2026"},
        json=payload
    )

    assert v1_response.status_code == 200
    assert v2_response.status_code == 200

    v1_data = v1_response.json()
    v2_data = v2_response.json()

    assert set(v1_data.keys()) == {
        "prediction",
        "confidence",
        "request_id"
    }

    assert set(v2_data.keys()) == {
        "prediction",
        "species_name",
        "confidence",
        "request_id"
    }

    assert "species_name" not in v1_data
    assert "species_name" in v2_data

    assert v1_data["prediction"] == v2_data["prediction"]
    assert 0 <= v1_data["confidence"] <= 1
    assert 0 <= v2_data["confidence"] <= 1

def test_predict_missing_api_key(client):
    response = client.post(
        "/api/v1/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 401

def test_predict_invalid_api_key(client):
    response = client.post(
        "/api/v1/predict",
        headers={"X-API-Key": "wrong-key"},
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 401

def test_predict_unexpected_field(client):
    response = client.post(
        "/api/v1/predict",
        headers={"X-API-Key": "iris-api-2026"},
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
            "extra_field": "not allowed"
        }
    )

    assert response.status_code == 422