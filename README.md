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






💻 How to Run This on Your Computer
Follow these steps to get the system running on your own machine.
What You Need First
Python 3.9 or newer installed.
Git installed.
Step 1: Download the CodeOpen your computer's terminal (or command prompt) and run:Bashgit clone [https://github.com/YOUR_USERNAME/supply-chain.git](https://github.com/YOUR_USERNAME/supply-chain.git)
cd supply-chain
Step 2: Set Up a Virtual WorkspaceThis keeps the project files separate from the rest of your computer.Bashpython -m venv venv

# If you are on Windows, run this to turn it on:
.\venv\Scripts\activate

# If you are on Mac/Linux, run this to turn it on:
source venv/bin/activate
Step 3: Install the Required SoftwareBashpip install -r requirements.txt
Step 4: Start the Background Server (Terminal 1)This server needs to stay running so the dashboard can talk
to the machine learning model.Bashuvicorn api.main:app --reload
The server is now listening at http://localhost:8000.
Step 5: Start the Web Dashboard (Terminal 2)Open a new, second terminal window. Go to the project folder, turn on the virtual workspace again, and run the dashboard:Bash# Windows
.\venv\Scripts\activate
streamlit run frontend/app.py

# Mac/Linux
source venv/bin/activate
streamlit run frontend/app.py
A web browser will automatically open to http://localhost:8501 where you can use the system.🔐 Test AccountsUse these accounts to log in and test the system:User TypeUsernamePasswordWhat They Can DoAdminadminadmin123Can use the dashboard and view the Audit LogsOperator 1operator1op1passCan only use the dashboard to check machinesOperator 2operator2op2passCan only use the dashboard to check machines🔮 Future ImprovementsLive Factory Data: Connect the system directly to real factory sensors instead of typing numbers in manually.Specific Error Types: Train the model to tell the user exactly what is breaking (e.g., "The motor is too hot" vs. "The tool is worn out").Cloud Hosting: Put the system on the internet using AWS or Google Cloud so anyone can access it without running code on their computer.
***

** Don't forget to change `YOUR_USERNAME` in Step 1 to your actual GitHub username before you commit this file!

With your codebase secure and your documentation looking top-tier, you are officially 
