from fastapi import APIRouter, Request

from app.models.schemas import PredictionInput, PredictionOutputV2


router = APIRouter(prefix="/api/v2")


@router.post("/predict", response_model=PredictionOutputV2)
def predict_v2(request: Request, data: PredictionInput):
    model = request.app.state.model
    request_id = request.state.request_id

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    prediction = model.predict(features)
    probabilities = model.predict_proba(features)

    confidence = float(max(probabilities[0]))

    species_names = {
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    }

    species_name = species_names[int(prediction[0])]

    return {
        "prediction": int(prediction[0]),
        "species_name": species_name,
        "confidence": confidence,
        "request_id": request_id
    }