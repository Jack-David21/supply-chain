# ⚙️ Predictive Maintenance Early-Warning System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688.svg)
![Random Forest](https://img.shields.io/badge/Random_Forest-scikit--learn-orange.svg)

**A Machine Learning Dashboard for Factory Floor Data**

When factory machines break down unexpectedly, it costs companies a lot of time and money. This project is a complete software system that predicts when equipment is going to fail *before* it actually happens, using data from machine sensors.

---

## 🚀 What It Does

Instead of waiting for a machine to break, this system acts as an early warning sign. It looks at real-time sensor readings (like how hot the machine is, how fast it is spinning, and how worn the tools are) and uses a Machine Learning model to spot hidden signs of failure.

### ✨ Key Features
*   **Smart Predictions:** Uses a Random Forest machine learning model trained on real factory data to predict machine breakdowns.
*   **Secure Logins:** Separate accounts for everyday operators and system administrators.
*   **Easy-to-Use Dashboard:** A web interface where users can enter sensor readings and instantly see if the machine is healthy or at risk.
*   **Two-Part System:** A secure backend server (FastAPI) handles the heavy math, while the frontend handles the user display.
*   **Activity Tracking (Audit Logs):** Keeps a permanent record of who checked a machine, what time they checked it, and what the prediction was. 
*   **Built-in Help Center:** Includes a documentation page explaining what each sensor does so new workers can understand the system.

---

## 📂 Project Layout

```text
predictive-supply-chain/
├── api/
│   ├── main.py                 # Backend API (FastAPI/Flask) for predictions
│   └── __init__.py             # Python package initialization
├── data/
│   ├── processed/              # Cleaned datasets ready for model input
│   ├── raw_data.csv            # Original factory dataset
│   ├── audit_log.csv           # System activity logs
│   └── tokenized_access_logs.csv # Security/Access data for anomaly detection
├── frontend/
│   └── static/
│       ├── app.js              # Dashboard logic and API integration
│       └── index.html          # Web interface for the supply chain dashboard
├── models/                     # Directory for saved .pkl or .joblib models
├── scripts/
│   ├── 1_eda_and_cleaning.py   # Data preprocessing and exploration
│   └── 2_model_training.py     # Model training and evaluation logic
├── .gitignore                  # Files to ignore in Git (e.g., venv, __pycache__)
├── README.md                   # Project documentation
└── req.txt                     # List of required Python dependencies
