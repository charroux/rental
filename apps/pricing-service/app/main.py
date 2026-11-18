from dataclasses import asdict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.pricing import calculate_quote

app = FastAPI(
    title="Rental Pricing Service",
    version="0.1.0",
    description="Standalone pricing service used by the DevOps course.",
)


class QuoteRequest(BaseModel):
    category: str = Field(min_length=1)
    days: int = Field(ge=1)


class QuoteResponse(BaseModel):
    category: str
    days: int
    daily_rate: float
    total: float
    currency: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "UP"}


@app.post("/quotes", response_model=QuoteResponse)
def create_quote(request: QuoteRequest) -> dict[str, object]:
    try:
        return asdict(calculate_quote(request.category, request.days))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
