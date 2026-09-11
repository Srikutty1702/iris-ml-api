from typing import List

from pydantic import BaseModel, Field, ConfigDict

class PredictionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sepal_length: float = Field(..., gt=0)
    sepal_width: float
    petal_length: float
    petal_width: float


class PredictionBatchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    inputs: List[PredictionInput] = Field(..., min_length=1)

class PredictionOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prediction: int

    confidence: float

    request_id: str


class PredictionBatchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    predictions: List[PredictionOutput]

class PredictionOutputV2(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prediction: int
    species_name: str
    confidence: float
    request_id: str