from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import joblib
import uuid
import time
from app.logging_config import logger
from app.routers.v1 import router as v1_router
from app.routers.v2 import router as v2_router
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading ML model...")

    app.state.model = joblib.load(settings.MODEL_PATH)

    logger.info("ML model loaded successfully.")

    yield

app = FastAPI(
    title=settings.API_TITLE,
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(v1_router)
app.include_router(v2_router)


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