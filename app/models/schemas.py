from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    sepal_length: float = Field(..., gt=0)
    sepal_width: float
    petal_length: float
    petal_width: float

class PredictionOutput(BaseModel):
    prediction: int
    confidence: float
    request_id: str