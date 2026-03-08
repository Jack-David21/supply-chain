"""
Phase 3 — FastAPI Backend
Predictive Maintenance Early-Warning System

Loads the trained XGBoost model and exposes a /predict endpoint that
accepts real-time sensor readings and returns a failure prediction.
"""

import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ──────────────────────────────────────────────
# 1. LOAD THE TRAINED MODEL (runs once at server startup)
# ──────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "xgboost_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise RuntimeError(
        f"Model file not found at {os.path.abspath(MODEL_PATH)}. "
        "Run Phase 2 (scripts/2_model_training.py) first to generate xgboost_model.pkl."
    )

# ──────────────────────────────────────────────
# 2. PYDANTIC SCHEMA — must mirror the features kept in Phase 1
# ──────────────────────────────────────────────
# Column names with spaces / brackets need aliases so the JSON payload
# uses the exact column names the model was trained on.

class SensorData(BaseModel):
    Type: int                          # 0 = Low, 1 = Medium, 2 = High quality
    air_temperature: float             # Air temperature [K]
    process_temperature: float         # Process temperature [K]
    rotational_speed: int              # Rotational speed [rpm]
    torque: float                      # Torque [Nm]
    tool_wear: int                     # Tool wear [min]

# The exact column order the XGBoost model expects (must match Phase 1).
FEATURE_COLUMNS = [
    "Type",
    "Air_temperature_K",
    "Process_temperature_K",
    "Rotational_speed_rpm",
    "Torque_Nm",
    "Tool_wear_min",
]

# ──────────────────────────────────────────────
# 3. FASTAPI APP
# ──────────────────────────────────────────────
app = FastAPI(
    title="Predictive Maintenance API",
    description="Real-time machine failure prediction from sensor telemetry.",
    version="1.0.0",
)


@app.get("/")
def root():
    """Health-check / welcome route."""
    return {"message": "Predictive Maintenance API is running."}


@app.post("/predict")
def predict(data: SensorData):
    """
    Accept a sensor reading and return a failure prediction.

    Returns
    -------
    dict with keys:
        prediction  – 0 (healthy) or 1 (failure)
        probability – model confidence for the failure class
        status      – human-readable verdict
    """
    try:
        # Convert the Pydantic payload into a single-row DataFrame whose
        # columns exactly match what the model was trained on.
        input_df = pd.DataFrame(
            [
                [
                    data.Type,
                    data.air_temperature,
                    data.process_temperature,
                    data.rotational_speed,
                    data.torque,
                    data.tool_wear,
                ]
            ],
            columns=FEATURE_COLUMNS,
        )

        # Binary prediction (0 or 1)
        prediction = int(model.predict(input_df)[0])

        # Probability for each class → we report P(failure)
        probability = float(model.predict_proba(input_df)[0][1])

        status = "Machine Failure Predicted" if prediction == 1 else "System Normal"

        return {
            "prediction": prediction,
            "probability": round(probability, 4),
            "status": status,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
