# Iris ML Prediction API

A beginner-friendly machine learning project that trains an Iris flower classification model and progressively exposes it through a FastAPI REST API.

## Project Overview

This project demonstrates the basic workflow of deploying a machine learning model as an API.

The project is being developed step by step:

1. Define the ML problem and API plan
2. Set up the Python development environment
3. Train and save an ML model
4. Build a basic FastAPI server
5. Connect the saved ML model to the API
6. Add input validation and testing
7. Prepare the API for deployment

## Dataset

The project uses the Iris flower dataset.

The model uses four input features:

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

The target is the Iris flower species.

The Iris dataset contains three classes:

- Iris Setosa
- Iris Versicolor
- Iris Virginica

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Scikit-learn
- Pandas
- Joblib
- Git
- GitHub

## Project Structure

```text
iris-ml-api/
│
├── app/
│   ├── main.py
│   ├── models/
│   └── routers/
│
├── ml/
│   ├── train.py
│   └── saved_model/
│       └── iris_model.pkl
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
