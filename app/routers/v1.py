from fastapi import APIRouter, Request, HTTPException,Depends
from app.models.schemas import (
    PredictionInput,
    PredictionOutput,
    PredictionBatchInput,
    PredictionBatchOutput,
)
from app.logging_config import logger
from app.config import settings
from app.security import verify_api_key
import time
import json

router = APIRouter(prefix="/api/v1")


@router.get("/health")
def health(request: Request):
    return {
        "status": "ok",
        "model_loaded": hasattr(request.app.state, "model")
    }


@router.post("/predict", response_model=PredictionOutput)
def predict(
    request: Request,
    data: PredictionInput,
    api_key: str = Depends(verify_api_key)
):
    model = request.app.state.model
    request_id = request.state.request_id

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    try:
        prediction = model.predict(features)
        probabilities = model.predict_proba(features)
        confidence = float(max(probabilities[0]))

        logger.info(
            f"Prediction successful | request_id={request_id} | "
            f"prediction={int(prediction[0])}"
        )

    except Exception as e:
        logger.error(
            f"Prediction failed | request_id={request_id} | error={e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

    return {
        "prediction": int(prediction[0]),
        "confidence": confidence,
        "request_id": request_id
    }


@router.post("/predict-batch", response_model=PredictionBatchOutput)
def predict_batch(request: Request, data: PredictionBatchInput):
    start_time = time.time()

    if len(data.inputs) > settings.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Batch size cannot exceed {settings.MAX_BATCH_SIZE}"
        )

    features = [
        [
            item.sepal_length,
            item.sepal_width,
            item.petal_length,
            item.petal_width
        ]
        for item in data.inputs
    ]

    model = request.app.state.model
    request_id = request.state.request_id

    prediction = model.predict(features)

    probabilities = model.predict_proba(features)

    confidences = [
        float(max(row))
        for row in probabilities
    ]

    results = [
        PredictionOutput(
            prediction=int(pred),
            confidence=confidence,
            request_id=request_id
        )
        for pred, confidence in zip(prediction, confidences)
    ]

    duration = time.time() - start_time

    logger.info(
        f"Batch prediction successful | request_id={request_id} | "
        f"batch_size={len(data.inputs)} | duration={duration:.4f}s"
    )

    return {
        "predictions": results
    }

@router.get("/model-info")
def model_info():
    with open("ml/saved_model/model_metadata.json", "r") as file:
        metadata = json.load(file)

    return metadata


# V2 plan: If the prediction response needs extra fields,
# create a new PredictionOutputV2 schema and a separate V2 router.
# Keep the existing V1 response unchanged so existing clients are not broken.