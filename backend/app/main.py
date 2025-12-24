from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://disaster_user:disaster_pass@localhost:5432/disaster_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)







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
    # Step 1: create prediction (dummy for now)
    result = DisasterOutput(
        disaster_type="flood",
        severity_score=0.82,
        risk_level="HIGH",
        population_at_risk=150000,
        confidence=0.90,
        timestamp=datetime.utcnow()
    )

    # Step 2: open DB session
    db = SessionLocal()

    # Step 3: insert into database
    insert_query = text("""
        INSERT INTO disasters (
            disaster_type,
            severity_score,
            risk_level,
            population_at_risk,
            confidence,
            location
        )
        VALUES (
            :disaster_type,
            :severity_score,
            :risk_level,
            :population_at_risk,
            :confidence,
            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
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
            "lat": data.latitude,
            "lon": data.longitude,
        }
    )

    db.commit()
    db.close()

    # Step 4: return response
    return result


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


@app.get("/disasters", response_model=list[DisasterRecord])
def get_disasters():
    db = SessionLocal()

    query = text("""
        SELECT
            id,
            disaster_type,
            severity_score,
            risk_level,
            population_at_risk,
            confidence,
            ST_Y(location::geometry) AS latitude,
            ST_X(location::geometry) AS longitude,
            created_at
        FROM disasters
        ORDER BY created_at DESC
    """)

    result = db.execute(query).fetchall()
    db.close()

    disasters = []
    for row in result:
        disasters.append(
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
        )

    return disasters


