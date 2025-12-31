import sys
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(PROJECT_ROOT)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db import SessionLocal, engine, Base
from app.models import disaster
from ml.inference.predict import run_inference


# -------------------------------------------------
# Create DB tables
# -------------------------------------------------
Base.metadata.create_all(bind=engine)
# -------------------------------------------------
# CLEAR OLD DATA ON SERVER START (DEMO MODE)
# -------------------------------------------------
db = SessionLocal()
db.execute(text("DELETE FROM disasters"))
db.commit()
db.close()


# -------------------------------------------------
# FastAPI app
# -------------------------------------------------
app = FastAPI(
    title="AI Disaster Intelligence Platform",
    description="Backend APIs for disaster detection and risk assessment",
    version="1.0.0"
)

# CORS (frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Schemas
# -------------------------------------------------
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


class DisasterRecord(BaseModel):
    id: int
    disaster_type: str
    severity_score: float
    risk_level: str
    population_at_risk: int
    confidence: float
    latitude: float
    longitude: float
    created_at: datetime

# -------------------------------------------------
# Health
# -------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -------------------------------------------------
# Predict Disaster (ML INFERENCE)
# -------------------------------------------------
@app.post("/predict/disaster", response_model=DisasterOutput)
def predict_disaster(data: DisasterInput):

    # 🔥 ML inference (ACTUAL FIX)
    prediction = run_inference(data.dict())

    result = DisasterOutput(
        disaster_type=prediction["disaster_type"],
        severity_score=prediction["severity_score"],
        risk_level=prediction["risk_level"],
        population_at_risk=prediction["population_at_risk"],
        confidence=prediction["confidence"],
        timestamp=datetime.utcnow()
    )

    # -------- Insert into DB --------
    db: Session = SessionLocal()

    insert_query = text("""
        INSERT INTO disasters (
            disaster_type,
            severity_score,
            risk_level,
            population_at_risk,
            confidence,
            latitude,
            longitude,
            created_at
        )
        VALUES (
            :disaster_type,
            :severity_score,
            :risk_level,
            :population_at_risk,
            :confidence,
            :latitude,
            :longitude,
            :created_at
        )
    """)

    db.execute(
        insert_query,
        {
            "disaster_type": result.disaster_type,
            "severity_score": result.severity_score,
            "risk_level": result.risk_level,
            "population_at_risk": result.population_at_risk,
            "confidence": result.confidence,
            "latitude": data.latitude,
            "longitude": data.longitude,
            "created_at": result.timestamp
        }
    )

    db.commit()
    db.close()

    return result

# -------------------------------------------------
# Get Disasters (for map markers)
# -------------------------------------------------
@app.get("/disasters", response_model=list[DisasterRecord])
def get_disasters():
    db: Session = SessionLocal()

    query = text("""
        SELECT
            id,
            disaster_type,
            severity_score,
            risk_level,
            population_at_risk,
            confidence,
            latitude,
            longitude,
            created_at
        FROM disasters
        ORDER BY created_at DESC
    """)

    rows = db.execute(query).fetchall()
    db.close()

    return [
        DisasterRecord(
            id=row.id,
            disaster_type=row.disaster_type,
            severity_score=row.severity_score,
            risk_level=row.risk_level,
            population_at_risk=row.population_at_risk,
            confidence=row.confidence,
            latitude=row.latitude,
            longitude=row.longitude,
            created_at=row.created_at
        )
        for row in rows
    ]
