# ⚙️ Predictive Maintenance Early-Warning System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-red.svg)

**A Machine Learning Dashboard for Factory Floor Data**

When factory machines break down unexpectedly, it costs companies a lot of time and money. This project is a complete software system that predicts when equipment is going to fail *before* it actually happens, using data from machine sensors.

---

## 🚀 What It Does

Instead of waiting for a machine to break, this system acts as an early warning sign. It looks at real-time sensor readings (like how hot the machine is, how fast it is spinning, and how worn the tools are) and uses a Machine Learning model to spot hidden signs of failure.

### ✨ Key Features
*   **Smart Predictions:** Uses an XGBoost machine learning model trained on real factory data to predict machine breakdowns.
*   **Secure Logins:** Separate accounts for everyday operators and system administrators.
*   **Easy-to-Use Dashboard:** A web interface where users can enter sensor readings and instantly see if the machine is healthy or at risk.
*   **Two-Part System:** A secure backend server (FastAPI) handles the heavy math, while the frontend (Streamlit) handles the user display.
*   **Activity Tracking (Audit Logs):** Keeps a permanent record of who checked a machine, what time they checked it, and what the prediction was. 
*   **Built-in Help Center:** Includes a documentation page explaining what each sensor does so new workers can understand the system.

---

## 📂 Project Layout

```text
predictive-supply-chain/
├── api/
│   └── main.py                 # The backend server that runs the predictions
├── data/
│   ├── processed/              # Cleaned data ready for the model
│   └── raw_data.csv            # The original factory dataset
├── frontend/
│   └── app.py                  # The web dashboard and login screens
├── models/
│   └── xgboost_model.pkl       # The saved machine learning model
├── scripts/
│   ├── 1_eda_and_cleaning.py   # Code used to clean the raw data
│   └── 2_model_training.py     # Code used to teach the model
├── requirements.txt            # List of required Python packages
└── README.md
