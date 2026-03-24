"""
FastAPI Backend
Predictive Maintenance Early-Warning System

Serves both the REST API predictions and the static HTML dashboard.
"""

import os
import joblib
import pandas as pd
import hashlib
import csv
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

# ──────────────────────────────────────────────
# 1. LOAD THE TRAINED MODEL
# ──────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "xgboost_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise RuntimeError(
        f"Model file not found at {os.path.abspath(MODEL_PATH)}. "
        "Run Phase 2 (scripts/2_model_training.py) first to generate xgboost_model.pkl."
    )

class SensorData(BaseModel):
    Type: int                          # 0 = Low, 1 = Medium, 2 = High quality
    air_temperature: float             # Air temperature [K]
    process_temperature: float         # Process temperature [K]
    rotational_speed: int              # Rotational speed [rpm]
    torque: float                      # Torque [Nm]
    tool_wear: int                     # Tool wear [min]

class PredictRequest(BaseModel):
    data: SensorData
    username: str
    role: str
    component_id: str

class LoginRequest(BaseModel):
    username: str
    password: str

FEATURE_COLUMNS = [
    "Type",
    "Air_temperature_K",
    "Process_temperature_K",
    "Rotational_speed_rpm",
    "Torque_Nm",
    "Tool_wear_min",
]

# ──────────────────────────────────────────────
# DEMO USERS AND AUDIT LOG
# ──────────────────────────────────────────────
def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

USERS = {
    "admin":     {"password_hash": _hash("admin123"),    "name": "Admin User",     "role": "Admin"},
    "operator1": {"password_hash": _hash("op1pass"),     "name": "Ram Kumar",      "role": "Operator"},
    "operator2": {"password_hash": _hash("op2pass"),     "name": "Priya Sharma",   "role": "Operator"},
    "engineer1": {"password_hash": _hash("eng1pass"),    "name": "Arjun Mehta",    "role": "Engineer"},
}

AUDIT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
AUDIT_FILE = os.path.join(AUDIT_DIR, "audit_log.csv")
AUDIT_COLUMNS = [
    "timestamp", "username", "role", "machine_id",
    "product_quality", "room_temp_K", "machine_temp_K",
    "spin_speed_rpm", "torque_Nm", "tool_wear_min",
    "prediction", "probability", "status",
]

def _ensure_audit_file():
    if not os.path.exists(AUDIT_FILE):
        os.makedirs(AUDIT_DIR, exist_ok=True)
        with open(AUDIT_FILE, "w", newline="") as f:
            csv.writer(f).writerow(AUDIT_COLUMNS)

def log_prediction(username, role, machine_id, data, prediction_result):
    _ensure_audit_file()
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        username,
        role,
        machine_id,
        data.Type,
        data.air_temperature,
        data.process_temperature,
        data.rotational_speed,
        data.torque,
        data.tool_wear,
        prediction_result["prediction"],
        prediction_result["probability"],
        prediction_result["status"],
    ]
    with open(AUDIT_FILE, "a", newline="") as f:
        csv.writer(f).writerow(row)

# ──────────────────────────────────────────────
# FASTAPI APP
# ──────────────────────────────────────────────
app = FastAPI(
    title="Predictive Maintenance API",
    description="Real-time machine failure prediction.",
    version="1.0.0",
)

@app.post("/api/login")
def login(creds: LoginRequest):
    user = USERS.get(creds.username)
    if user and user["password_hash"] == _hash(creds.password):
        return {"success": True, "username": creds.username, "display_name": user["name"], "role": user["role"]}
    raise HTTPException(status_code=401, detail="Invalid username or password.")

@app.post("/api/predict")
def predict(request: PredictRequest):
    try:
        data = request.data
        input_df = pd.DataFrame(
            [[data.Type, data.air_temperature, data.process_temperature, data.rotational_speed, data.torque, data.tool_wear]],
            columns=FEATURE_COLUMNS,
        )

        prediction = int(model.predict(input_df)[0])
        probability = float(model.predict_proba(input_df)[0][1])
        status = "Machine Failure Predicted" if prediction == 1 else "System Normal"
        
        result = {
            "prediction": prediction,
            "probability": round(probability, 4),
            "status": status,
        }
        
        log_prediction(request.username, request.role, request.component_id, data, result)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/api/audit-log")
def get_audit_log():
    _ensure_audit_file()
    try:
        df = pd.read_csv(AUDIT_FILE)
        return df.to_dict(orient="records")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

# Serve static files as the main frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "static")
if not os.path.exists(frontend_dir):
    os.makedirs(frontend_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
