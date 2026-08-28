from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
import joblib
from app.models.schemas import PredictionInput, PredictionOutput
import uuid
import time
from app.logging_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading ML model...")

    app.state.model = joblib.load("ml/saved_model/iris_model.pkl")

    logger.info("ML model loaded successfully.")

    yield


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"Request completed | request_id={request_id} | "
        f"method={request.method} | path={request.url.path} | "
        f"duration={duration:.4f}s | status={response.status_code}"
    )

    return response


@app.get("/")
def root():
    return {"message": "ML API is alive"}


@app.get("/health")
def health(request: Request):
    return {
        "status": "ok",
        "model_loaded": hasattr(request.app.state, "model")
    }


@app.post("/predict", response_model=PredictionOutput)
def predict(request: Request, data: PredictionInput):
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