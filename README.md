Iris ML Prediction API

A beginner-friendly machine learning deployment project that trains an Iris flower classification model and exposes it through a monitored FastAPI REST API.

The project demonstrates how a trained machine learning model can be packaged, served through an API, validated, tested, monitored, and containerized using Docker.

Project Overview

This project follows the complete workflow of deploying a machine learning model as a REST API.

The main components include:

Machine learning model training

FastAPI REST API

Input and response validation

API versioning

API-key authentication for prediction endpoints

Structured logging

Prometheus monitoring

Automated testing

Integration testing

Basic concurrent load testing

Docker containerization

Docker Compose

Public cloud deployment using Render

Grafana + Prometheus monitoring extension

Machine Learning Model

The project uses the Iris flower dataset.

The model is a classification model trained using Scikit-learn.

Input Features

The model uses four features:

Sepal Length

Sepal Width

Petal Length

Petal Width

Target Classes

The model predicts one of three Iris flower classes:

Iris Setosa

Iris Versicolor

Iris Virginica

The trained model is saved using Joblib and loaded by the FastAPI application when the application starts.

Technologies Used

Python

FastAPI

Uvicorn

Scikit-learn

Pandas

Joblib

Pydantic

Pydantic Settings

Prometheus

prometheus-fastapi-instrumentator

pytest

Requests

Docker

Docker Compose

Git

GitHub

Project Architecture

Client
   |
   | HTTP Request
   v
FastAPI Application
   |
   +----------------------+
   |                      |
   v                      v
Authentication        Input Validation
(X-API-Key)           (Pydantic)
   |                      |
   +----------+-----------+
              |
              v
        API Router
        /api/v1
        /api/v2
              |
              v
        Saved ML Model
        iris_model.pkl
              |
              v
          Prediction
              |
              v
     JSON Response
              |
              +------------------+
              |                  |
              v                  v
           Logging          Prometheus
                            /metrics

Project Structure

iris-ml-api/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── logging_config.py
│   ├── security.py
│   │   │
│   ├── models/
│   │   └── schemas.py
│   │
│   └── routers/
│       ├── v1.py
│       └── v2.py
│
├── ml/
│   └── saved_model/
│       ├── iris_model.pkl
│       └── model_metadata.json
│
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_model_info.py
│   └── test_predict.py
│
├── train.py
├── load_test.py
├── metrics.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── TESTING.md
└── README.md

API Endpoints

API V1

Method

Endpoint

Purpose

GET

/api/v1/health

Check API and model health

POST

/api/v1/predict

Predict one Iris flower

POST

/api/v1/predict-batch

Predict multiple Iris flowers

GET

/api/v1/model-info

View information about the serving model

API V2

Method

Endpoint

Purpose

POST

/api/v2/predict

Predict with species name included

Monitoring

Method

Endpoint

Purpose

GET

/metrics

Prometheus monitoring metrics

API Authentication

Prediction endpoints use an API key for authentication.

The API key is supplied through the X-API-Key request header.

Example:

X-API-Key: your-secret-api-key

The actual API key is stored in the .env file and is not committed to Git.

Example .env configuration:

MODEL_PATH=ml/saved_model/iris_model.pkl
LOG_LEVEL=INFO
MAX_BATCH_SIZE=100
API_TITLE=ML Model Deployment as a Monitored REST API
API_KEY=your-secret-api-key

The .env.example file contains a placeholder value for sharing the project structure safely.

Input Validation

The API uses Pydantic schemas to validate incoming requests.

The prediction input contains:

{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}

Unexpected fields are rejected using Pydantic's extra="forbid" configuration.

Invalid requests return an HTTP 422 validation error.

Requests with a missing or invalid API key on protected prediction endpoints return HTTP 401.

Example API Requests

Root Endpoint

curl http://localhost:8000/

Example response:

{
  "message": "ML API is alive"
}

Health Check

curl http://localhost:8000/api/v1/health

Single Prediction

curl -X POST "http://localhost:8000/api/v1/predict" \
-H "X-API-Key: your-secret-api-key" \
-H "Content-Type: application/json" \
-d '{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}'

Example response:

{
  "prediction": 0,
  "confidence": 0.976,
  "request_id": "example-request-id"
}

Batch Prediction

curl -X POST "http://localhost:8000/api/v1/predict-batch" \
-H "X-API-Key: your-secret-api-key" \
-H "Content-Type: application/json" \
-d '{
  "inputs": [
    {
      "sepal_length": 5.1,
      "sepal_width": 3.5,
      "petal_length": 1.4,
      "petal_width": 0.2
    },
    {
      "sepal_length": 6.7,
      "sepal_width": 3.1,
      "petal_length": 4.7,
      "petal_width": 1.5
    }
  ]
}'

The batch endpoint processes multiple Iris inputs in a single request.

Model Information

curl http://localhost:8000/api/v1/model-info

This endpoint provides information about the model currently being used by the API.

Metrics

curl http://localhost:8000/metrics

The endpoint returns Prometheus-formatted monitoring metrics.

V2 Prediction

curl -X POST "http://localhost:8000/api/v2/predict" \
-H "X-API-Key: your-secret-api-key" \
-H "Content-Type: application/json" \
-d '{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}'

V2 extends the prediction response by including the predicted species name.

Live Deployment

Public API:

https://iris-ml-api-41kq.onrender.com

Swagger Documentation:

https://iris-ml-api-41kq.onrender.com/docs

API Documentation

When the application is running, interactive Swagger documentation is available at:

http://localhost:8000/docs

The OpenAPI specification is available locally at:

http://localhost:8000/openapi.json

For the deployed API:

https://iris-ml-api-41kq.onrender.com/openapi.json

Monitoring

The API is instrumented using Prometheus-compatible monitoring.

The /metrics endpoint exposes live metrics such as:

Total HTTP requests

HTTP request status codes

Request information by endpoint

Request latency metrics

Python process metrics

Memory usage

CPU usage

Custom Iris prediction metrics

Example:

http://localhost:8000/metrics

Custom ML Metric

The project includes a custom Prometheus counter:

iris_predictions_total

This metric records successful Iris predictions and uses the predicted class as a label.

Example:

iris_predictions_total{prediction_class="0"} 51.0

This allows the prediction activity of the machine learning API to be monitored separately from general HTTP traffic.

Logging

The project uses centralized logging configuration.

Logging records important application events such as:

ML model loading

Successful model loading

API requests

Request IDs

Request methods

Request paths

Response status codes

Request duration

A request ID is generated for each request to help trace requests through the application.

Sensitive client information should not be written to logs.

API Versioning

The project supports multiple API versions.

V1

/api/v1/

V2

/api/v2/

API versioning allows the API to evolve while maintaining compatibility with existing clients.

V2 demonstrates an extended prediction response that includes the species name while preserving the existing V1 API.

Testing

The project uses pytest for automated testing.

The test suite covers:

Health endpoint

Prediction endpoint

Input validation

Batch prediction

Model information

Missing API key

Invalid API key

Unexpected input fields

Run the automated tests with:

pytest

Current test result:

10 passed

Integration Testing

Integration testing verifies the complete application through the running Docker container.

The integration checks cover:

/api/v1/health

/api/v1/predict

/api/v1/predict-batch

/metrics

The tests communicate with the running application through HTTP requests instead of using FastAPI's internal TestClient.

Detailed testing information is documented in:

TESTING.md

Load Testing

A basic concurrent load test was performed using:

load_test.py

Test configuration:

Concurrent requests: 50
Endpoint: /api/v1/predict
Request type: POST
Authentication: X-API-Key

Test result:

Total requests: 50
Successful requests: 50
Failed requests: 0

The load test was used to verify that the containerized API could successfully process multiple concurrent prediction requests.

Docker

The application is containerized using Docker.

Build the Docker Image

docker build -t ml-api:v1 .

Run the Docker Container

docker run --env-file .env -p 8000:8000 ml-api:v1

The API will then be available at:

http://localhost:8000

Docker Compose

Docker Compose simplifies running the application and its configuration.

Start the application with:

docker compose up --build

Open the API documentation:

http://localhost:8000/docs

Stop the application with:

docker compose down

Environment Configuration

Application configuration is stored using environment variables.

The project uses:

.env

for local configuration.

The following values are configured:

MODEL_PATH
LOG_LEVEL
MAX_BATCH_SIZE
API_TITLE
API_KEY

The .env file is excluded from Git using .gitignore.

The repository contains .env.example as a safe configuration template.

Security

The project includes basic API security features:

API-key authentication

Environment-based secret configuration

Request validation

Rejection of unexpected request fields

CORS configuration

.env excluded from Git

The API key protects the prediction endpoints and is separate from Docker container security.

Running the Project Locally

1. Create and activate a virtual environment

python -m venv venv

Windows:

venv\Scripts\activate

2. Install dependencies

pip install -r requirements.txt

3. Configure environment variables

Create a .env file in the project root.

Example:

MODEL_PATH=ml/saved_model/iris_model.pkl
LOG_LEVEL=INFO
MAX_BATCH_SIZE=100
API_TITLE=ML Model Deployment as a Monitored REST API
API_KEY=your-secret-api-key

4. Start the API

uvicorn app.main:app --reload

5. Open Swagger

http://localhost:8000/docs

Running with Docker Compose

Make sure Docker Desktop is running.

Start the application:

docker compose up --build

Open:

http://localhost:8000/docs

To stop:

docker compose down

What I Learned

Through this project, I learned the complete basic workflow of deploying a machine learning model as a REST API.

Machine Learning

Dataset preparation

Features and target

Train/test split

Model training

Model saving

Loading a saved model

Prediction and confidence

FastAPI

FastAPI application structure

API endpoints

Request and response models

Pydantic validation

Routers

API versioning

Lifespan events

Middleware

Security

API-key authentication

Environment variables

CORS

Input validation

Testing

pytest

Unit testing

Integration testing

Concurrent load testing

Automated verification

Monitoring

Prometheus

Counters

Gauges

Histograms

Summaries

HTTP request metrics

Custom machine learning metrics

Deployment

Docker

Docker images

Docker containers

Docker Compose

Environment configuration

Development Workflow

Git

GitHub

Commits

Branch management

Rebase

Push and pull

.gitignore

Independent Extension — Grafana + Prometheus

Implemented Grafana and Prometheus monitoring for the Iris ML API.

Monitoring Architecture

FastAPI API → Prometheus → Grafana

Prometheus

Prometheus scrapes the FastAPI /metrics endpoint every 5 seconds.

Target:

api:8000/metrics

Grafana Dashboard

Created a Grafana dashboard named Iris ML API Monitoring with:

Total Iris Predictions — displays the custom iris_predictions_total ML metric.

API Request Rate — displays the API request rate using Prometheus HTTP metrics.

Result

The monitoring setup allows API activity and ML prediction activity to be visualized through Grafana using metrics collected by Prometheus.

The Grafana and Prometheus extension is configured through the local Docker Compose monitoring stack. The public Render deployment hosts the FastAPI API separately.

Future Improvements

Possible future improvements include:

Adding GitHub Actions for CI/CD

Adding model retraining

Adding response caching

Adding more comprehensive load testing

Adding production-grade authentication

Adding database integration

Project Status

The project currently includes:

Iris ML model training

Saved ML model

FastAPI REST API

Pydantic validation

API versioning

API-key authentication

Request logging

Prometheus monitoring

Custom ML metric

Automated tests

Integration testing

Concurrent load testing

Docker containerization

Docker Compose

Public cloud deployment

Independent extension

Final project polish

Author

Srivarsha

B.Sc. Computer Science

