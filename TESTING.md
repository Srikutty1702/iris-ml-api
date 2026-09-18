# Testing

## Integration Testing

The API was tested through the running Docker container using HTTP requests.

The following endpoints were verified:

- `GET /api/v1/health`
- `POST /api/v1/predict`
- `POST /api/v1/predict-batch`
- `GET /metrics`

The health endpoint returned `200 OK` and confirmed that the ML model was loaded.

The prediction endpoint successfully returned predictions with confidence and request ID.

The batch prediction endpoint successfully processed multiple Iris inputs.

The `/metrics` endpoint returned valid Prometheus metrics.

## Load Testing

A basic concurrent load test was performed using `load_test.py`.

Test configuration:

- Concurrent requests: 50
- Endpoint: `/api/v1/predict`
- Authentication: `X-API-Key`
- Request type: POST

Results:

- Total requests: 50
- Successful requests: 50
- Failed requests: 0

The Prometheus metrics were checked after the load test.

The custom `iris_predictions_total` metric increased from 1 to 51, confirming that the successful predictions were recorded.

## Bug Fixed

### Missing `requests` Dependency

The load-test script uses the Python `requests` library. Initially, the dependency was installed manually but was not listed in `requirements.txt`.

This was fixed by adding:

```text
requests
```
