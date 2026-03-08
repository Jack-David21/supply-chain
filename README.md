# ⚙️ Predictive Maintenance Early-Warning System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-red.svg)

**A B2B Machine Learning Dashboard for Factory Floor IoT Data**  
*Built during a 48-Hour Hackathon*

Unplanned machine downtime costs manufacturing facilities millions of dollars annually. This project is an end-to-end Machine Learning pipeline and full-stack dashboard designed to predict factory equipment failures *before* they occur using high-frequency IoT sensor data.

---

## 🚀 The Solution & Features

Instead of reacting to broken machines, our system provides an early-warning API and operator dashboard. It ingests real-time sensor readings (temperature, rotational speed, torque, and tool wear) and uses an XGBoost classifier optimized for high recall to flag anomalous patterns.

*   **Real-Time ML Predictions:** Powered by an XGBoost model trained on imbalanced factory failure data.
*   **Role-Based Access Control:** Secure operator and administrator login tiers.
*   **Interactive Dashboard:** Built with Streamlit, allowing operators to manually input or simulate sensor readings.
*   **Decoupled Architecture:** A standalone FastAPI backend serving the `.pkl` model, completely separated from the frontend.
*   **Enterprise Audit Logging:** Tracks exactly *who* ran a diagnostic check, *when*, and the predicted outcome—ensuring full accountability.
*   **Documentation Hub:** Built-in equipment and sensor explanations for operator onboarding.

---

## 📂 Project Architecture

```text
predictive-supply-chain/
├── api/
│   └── main.py                 # FastAPI server & prediction endpoint
├── data/
│   ├── processed/              # Cleaned X_train, y_train datasets
│   └── raw_data.csv            # Original Kaggle dataset
├── frontend/
│   └── app.py                  # Streamlit UI, Auth, & Logic
├── models/
│   └── xgboost_model.pkl       # Serialized ML model
├── scripts/
│   ├── 1_eda_and_cleaning.py   # Data preparation pipeline
│   └── 2_model_training.py     # Model training & evaluation
├── requirements.txt            # Pinned dependencies
└── README.md
