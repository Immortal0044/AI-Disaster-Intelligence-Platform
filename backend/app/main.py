from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="AI Disaster Intelligence Platform",
    description="Backend APIs for disaster detection and risk assessment",
    version="1.0.0"
)

# ------------------ Schemas ------------------

class DisasterInput(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime
    weather_rainfall: float | None = None
    weather_wind_speed: float | None = None
    social_signal_score: float | None = None


class DisasterOutput(BaseModel):
    disaster_type: str
    severity_score: float
    risk_level: str
    population_at_risk: int
    confidence: float
    timestamp: datetime


# ------------------ Routes ------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict/disaster", response_model=DisasterOutput)
def predict_disaster(data: DisasterInput):
    return DisasterOutput(
        disaster_type="flood",
        severity_score=0.82,
        risk_level="HIGH",
        population_at_risk=150000,
        confidence=0.90,
        timestamp=datetime.utcnow()
    )
