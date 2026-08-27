import os
import joblib
import numpy as np
from typing import Optional
from dataclasses import dataclass


MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "models", "disruption_model.pkl")

_model = None


@dataclass
class DisruptionPrediction:
    risk_score: float
    risk_level: str
    contributing_factors: list[str]


def _load_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    return _model


FEATURE_NAMES = [
    "rainfall_1h", "rainfall_24h", "rainfall_7d",
    "slope_deg", "elevation_m", "road_surface",
    "historical_landslides", "soil_moisture", "distance_to_river_km",
]


def predict_disruption(
    rainfall_1h: float = 0,
    rainfall_24h: float = 0,
    rainfall_7d: float = 0,
    slope_deg: float = 15,
    elevation_m: float = 500,
    road_surface: int = 1,
    historical_landslides: int = 0,
    soil_moisture: float = 0.3,
    distance_to_river_km: float = 5.0,
) -> Optional[DisruptionPrediction]:
    model = _load_model()
    if model is None:
        risk = _heuristic_risk(
            rainfall_1h, rainfall_24h, rainfall_7d,
            slope_deg, soil_moisture, historical_landslides, distance_to_river_km
        )
        return DisruptionPrediction(
            risk_score=risk,
            risk_level=_risk_level(risk),
            contributing_factors=_get_factors(
                rainfall_1h, rainfall_24h, rainfall_7d,
                slope_deg, soil_moisture, historical_landslides, distance_to_river_km
            ),
        )

    import pandas as pd
    features = pd.DataFrame([[
        rainfall_1h, rainfall_24h, rainfall_7d,
        slope_deg, elevation_m, road_surface,
        historical_landslides, soil_moisture, distance_to_river_km,
    ]], columns=FEATURE_NAMES)

    xgb_prob = model["xgb"].predict_proba(features)[0][1]
    rf_prob = model["rf"].predict_proba(features)[0][1]
    risk = float(0.6 * xgb_prob + 0.4 * rf_prob)

    return DisruptionPrediction(
        risk_score=round(risk, 3),
        risk_level=_risk_level(risk),
        contributing_factors=_get_factors(
            rainfall_1h, rainfall_24h, rainfall_7d,
            slope_deg, soil_moisture, historical_landslides, distance_to_river_km
        ),
    )


def _heuristic_risk(r1, r24, r7d, slope, moisture, hist, river_dist):
    score = 0.0
    if r24 > 50: score += 0.35
    elif r24 > 20: score += 0.15
    if slope > 25: score += 0.25
    elif slope > 15: score += 0.10
    if r7d > 150: score += 0.15
    elif r7d > 50: score += 0.05
    if moisture > 0.6: score += 0.10
    if hist > 2: score += 0.08
    if river_dist < 1: score += 0.07
    return min(score, 1.0)


def _risk_level(score: float) -> str:
    if score >= 0.7: return "critical"
    if score >= 0.5: return "high"
    if score >= 0.3: return "moderate"
    return "low"


def _get_factors(r1, r24, r7d, slope, moisture, hist, river_dist):
    factors = []
    if r24 > 20: factors.append(f"Heavy rainfall ({r24:.0f}mm/24h)")
    if r7d > 50: factors.append(f"Persistent rain ({r7d:.0f}mm/7d)")
    if slope > 20: factors.append(f"Steep terrain ({slope:.0f}°)")
    if moisture > 0.5: factors.append(f"High soil moisture ({moisture:.0%})")
    if hist > 1: factors.append(f"History of {hist} landslides")
    if river_dist < 2: factors.append(f"Near river ({river_dist:.1f}km)")
    return factors
