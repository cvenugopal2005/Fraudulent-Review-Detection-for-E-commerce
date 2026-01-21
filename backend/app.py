from fastapi import FastAPI
from pydantic import BaseModel
from backend.model_utils import predict_review

app = FastAPI(
    title="Fraudulent Review Detection API",
    description="AI-based system to detect fake product reviews",
    version="1.0"
)

class ReviewInput(BaseModel):
    review: str

@app.post("/predict")
def predict(data: ReviewInput):
    return predict_review(data.review)
