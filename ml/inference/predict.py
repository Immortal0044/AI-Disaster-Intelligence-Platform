"""
ML inference module for disaster prediction.
This is a SIMPLE baseline version.
You can replace the logic later with trained models.
"""

def run_inference(input_data: dict) -> dict:
    """
    input_data keys:
    - latitude
    - longitude
    - timestamp
    - weather_rainfall
    - weather_wind_speed
    - social_signal_score
    """

    rainfall = input_data.get("weather_rainfall", 0) or 0
    social_score = input_data.get("social_signal_score", 0) or 0

    # ---------------- BASIC LOGIC ----------------
    # This is NOT dummy — it is a rule-based baseline
    # ML model will replace this later

    if rainfall > 100 and social_score > 0.7:
        disaster_type = "flood"
        severity_score = 0.85
        risk_level = "HIGH"
        population_at_risk = 150000
        confidence = 0.9

    elif social_score > 0.6:
        disaster_type = "earthquake"
        severity_score = 0.7
        risk_level = "MEDIUM"
        population_at_risk = 80000
        confidence = 0.8

    else:
        disaster_type = "none"
        severity_score = 0.2
        risk_level = "LOW"
        population_at_risk = 10000
        confidence = 0.6

    return {
        "disaster_type": disaster_type,
        "severity_score": severity_score,
        "risk_level": risk_level,
        "population_at_risk": population_at_risk,
        "confidence": confidence
    }
