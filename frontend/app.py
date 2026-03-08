"""
Phase 4 — Streamlit Frontend Dashboard
Predictive Maintenance Early-Warning System

Provides a visual interface for operators to enter live sensor readings
and receive an instant failure prediction from the FastAPI backend.
Includes login, audit logging, and an Info page.
"""

import os
import hashlib
import csv
from datetime import datetime

import streamlit as st
import requests
import pandas as pd

# ──────────────────────────────────────────────
# 1. PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Predictive Maintenance Early-Warning System",
    page_icon="⚙️",
    layout="wide",
)

# ──────────────────────────────────────────────
# AUDIT LOG HELPERS
# ──────────────────────────────────────────────
AUDIT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
AUDIT_FILE = os.path.join(AUDIT_DIR, "audit_log.csv")
AUDIT_COLUMNS = [
    "timestamp", "username", "role", "machine_id",
    "product_quality", "room_temp_K", "machine_temp_K",
    "spin_speed_rpm", "torque_Nm", "tool_wear_min",
    "prediction", "probability", "status",
]


def _ensure_audit_file():
    """Create the audit CSV with a header row if it doesn't exist."""
    if not os.path.exists(AUDIT_FILE):
        os.makedirs(AUDIT_DIR, exist_ok=True)
        with open(AUDIT_FILE, "w", newline="") as f:
            csv.writer(f).writerow(AUDIT_COLUMNS)


def log_prediction(username, role, machine_id, inputs, result):
    """Append one row to the audit log."""
    _ensure_audit_file()
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        username,
        role,
        machine_id,
        inputs["Type"],
        inputs["air_temperature"],
        inputs["process_temperature"],
        inputs["rotational_speed"],
        inputs["torque"],
        inputs["tool_wear"],
        result["prediction"],
        result["probability"],
        result["status"],
    ]
    with open(AUDIT_FILE, "a", newline="") as f:
        csv.writer(f).writerow(row)


# ──────────────────────────────────────────────
# DEMO COMPANY CREDENTIALS
# ──────────────────────────────────────────────
# For this MVP, credentials are stored here.
# Passwords are SHA-256 hashed. Replace with a real auth provider in prod.
def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


USERS = {
    "admin":    {"password_hash": _hash("admin123"),    "name": "Admin User",      "role": "Admin"},
    "operator1": {"password_hash": _hash("op1pass"),    "name": "Ram Kumar",   "role": "Operator"},
    "operator2": {"password_hash": _hash("op2pass"),    "name": "Priya Sharma",  "role": "Operator"},
    "engineer1": {"password_hash": _hash("eng1pass"),   "name": "Arjun Mehta", "role": "Engineer"},
}

# ──────────────────────────────────────────────
# LOGIN SCREEN
# ──────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.display_name = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🔐 Company Login</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;'>Sign in with your company credentials to continue.</p>",
        unsafe_allow_html=True,
    )

    _, form_col, _ = st.columns([1, 1.5, 1])
    with form_col:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In", use_container_width=True)

        if submitted:
            user = USERS.get(username)
            if user and user["password_hash"] == _hash(password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.display_name = user["name"]
                st.session_state.role = user["role"]
                st.rerun()
            else:
                st.error("Invalid username or password.")

        st.divider()
        st.markdown(
            "**Demo accounts for MVP:**\n"
            "| Username | Password | Role |\n"
            "|----------|----------|------|\n"
            "| admin | admin123 | Admin |\n"
            "| operator1 | op1pass | Operator |\n"
            "| operator2 | op2pass | Operator |\n"
            "| engineer1 | eng1pass | Engineer |"
        )

    st.stop()

# ══════════════════════════════════════════════
#  AUTHENTICATED — MAIN APP BELOW
# ══════════════════════════════════════════════

# ──────────────────────────────────────────────
# 2. TOP BAR — title left, user info + nav right
# ──────────────────────────────────────────────
title_col, nav_col = st.columns([5, 1])

with title_col:
    st.title("⚙️ Predictive Maintenance Early-Warning System")

with nav_col:
    st.markdown("")
    pages = ["🏠 Dashboard", "ℹ️ Info", "📒 Audit Log"]
    page = st.selectbox(
        "Navigate",
        options=pages,
        label_visibility="collapsed",
    )


# ======================================================================
#  INFO PAGE
# ======================================================================
if page == "ℹ️ Info":
    st.divider()
    st.header("ℹ️ About Our Equipment")
    st.markdown(
        "This page explains the machines, sensors, and tools that our system monitors. "
        "Read through it to understand what each reading means and why it matters."
    )

    # --- Machine overview ---
    st.subheader("🏭 The Machine")
    st.markdown(
        """
        We use a **CNC milling machine** — a computer-controlled cutting machine on the factory floor.
        Every time it runs, we record the conditions around it and how it's performing.
        The machine makes parts in three quality levels:
        - **Low** — basic, everyday parts
        - **Medium** — standard parts
        - **High** — precision parts that need extra care
        """
    )

    # --- Sensor descriptions ---
    st.subheader("📡 The Sensors")

    sensors = [
        {
            "Sensor": "🌡️ Room Temperature Sensor",
            "What it measures": "How warm or cool the air is around the machine",
            "Unit": "Kelvin (°K)",
            "Typical range": "295 – 305 °K",
            "Why it matters": "If the room is too hot, the machine can overheat and break down faster.",
        },
        {
            "Sensor": "🔥 Machine Temperature Sensor",
            "What it measures": "How hot the machine itself is getting during work",
            "Unit": "Kelvin (°K)",
            "Typical range": "306 – 314 °K",
            "Why it matters": "When the machine gets too hot inside, it means something is rubbing too hard — a sign of trouble.",
        },
        {
            "Sensor": "🔄 Spin Speed Sensor",
            "What it measures": "How fast the main spinning part (spindle) is turning",
            "Unit": "RPM (turns per minute)",
            "Typical range": "1,200 – 2,900 RPM",
            "Why it matters": "If it spins too fast or too slow compared to normal, something could be wearing out.",
        },
        {
            "Sensor": "💪 Twisting Force Sensor",
            "What it measures": "How hard the machine is pushing to cut the material",
            "Unit": "Nm (Newton-metres)",
            "Typical range": "3 – 77 Nm",
            "Why it matters": "A sudden jump in force usually means the tool is stuck or the material is too tough.",
        },
        {
            "Sensor": "⏱️ Tool Usage Counter",
            "What it measures": "How many minutes the current cutting tool has been in use",
            "Unit": "Minutes",
            "Typical range": "0 – 253 minutes",
            "Why it matters": "Old tools get dull and can snap. Replacing them on time prevents breakdowns.",
        },
    ]

    for s in sensors:
        with st.expander(s["Sensor"], expanded=False):
            col_a, col_b = st.columns(2)
            col_a.markdown(f"**What it measures:** {s['What it measures']}")
            col_a.markdown(f"**Unit:** {s['Unit']}")
            col_b.markdown(f"**Typical range:** {s['Typical range']}")
            col_b.markdown(f"**Why it matters:** {s['Why it matters']}")

    # --- Failure modes ---
    st.subheader("⚠️ What Can Go Wrong")
    st.markdown(
        """
        The machine can break down in five different ways. Our system checks for
        **all of them at once** and warns you before it happens.

        | Short Name | What It Means | How It Happens |
        |------|-------------|-------------|
        | **TWF** | Tool Wore Out | The cutting tool has been used too long and is no longer sharp enough. |
        | **HDF** | Too Hot | The machine can't cool down fast enough and overheats. |
        | **PWF** | Too Much Power | The machine is spinning and pushing harder than it safely should. |
        | **OSF** | Pushed Too Hard | A worn-out tool combined with high force — the machine is overstrained. |
        | **RNF** | Random Breakdown | A rare, unpredictable problem (happens roughly 1 in 1,000 runs). |
        """
    )

    # --- Product quality tiers ---
    st.subheader("📦 Product Quality Levels")
    st.markdown(
        """
        | Level | Letter | How Common | What's Different |
        |------|-------|--------------------:|------------------|
        | **Low** | L | ~60 % of all runs | Faster cutting, less force — for basic parts. |
        | **Medium** | M | ~30 % of all runs | Balanced speed and force — for everyday parts. |
        | **High** | H | ~10 % of all runs | Slower, stronger cuts — for parts that need to be very precise. |
        """
    )

    st.info(
        "💡 **Tip:** Use the dropdown in the top-right corner to go back to the Dashboard.",
        icon="💡",
    )


# ======================================================================
#  AUDIT LOG PAGE
# ======================================================================
elif page == "📒 Audit Log":
    st.divider()
    st.header("📒 Audit Log")
    st.markdown("This page shows a record of every check that has been done — who did it, which equipment was checked, what values were entered, and what the system found.")

    _ensure_audit_file()

    if os.path.exists(AUDIT_FILE):
        df_log = pd.read_csv(AUDIT_FILE)
        if df_log.empty:
            st.info("No checks have been recorded yet. Go to the Dashboard and run a check first.")
        else:
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            with filter_col1:
                users_available = ["All"] + sorted(df_log["username"].dropna().unique().tolist())
                user_filter = st.selectbox("Show entries by", users_available)
            with filter_col2:
                machines_available = ["All"] + sorted(df_log["machine_id"].dropna().unique().tolist())
                machine_filter = st.selectbox("Show entries for equipment", machines_available)
            with filter_col3:
                status_available = ["All"] + sorted(df_log["status"].dropna().unique().tolist())
                status_filter = st.selectbox("Show by result", status_available)

            filtered = df_log.copy()
            if user_filter != "All":
                filtered = filtered[filtered["username"] == user_filter]
            if machine_filter != "All":
                filtered = filtered[filtered["machine_id"] == machine_filter]
            if status_filter != "All":
                filtered = filtered[filtered["status"] == status_filter]

            st.dataframe(filtered.sort_values("timestamp", ascending=False), use_container_width=True)
            st.caption(f"Showing {len(filtered)} of {len(df_log)} total records.")
    else:
        st.info("No records found yet. Go to the Dashboard and run a check to start recording.")


# ======================================================================
#  DASHBOARD PAGE (default)
# ======================================================================
else:
    st.markdown(
        "Select the equipment, enter the readings, and press **Run Check**."
    )
    st.divider()

    # ──────────────────────────────────────────────
    # 3. SIDEBAR — EQUIPMENT & READINGS
    # ──────────────────────────────────────────────
    st.sidebar.markdown(
        f"👤 **{st.session_state.display_name}**  \n"
        f"_{st.session_state.role}_"
    )
    if st.sidebar.button("Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.rerun()
    st.sidebar.divider()
    st.sidebar.header("🔧 Equipment & Readings")

    component_type = st.sidebar.selectbox(
        "Equipment Type",
        options=["Machine", "Sensor", "Cutting Tool"],
    )

    if component_type == "Machine":
        component_id = st.sidebar.text_input("Machine ID", value="CNC-001")
    elif component_type == "Sensor":
        component_id = st.sidebar.text_input("Sensor ID", value="TEMP-001")
    else:
        component_id = st.sidebar.text_input("Tool ID", value="TOOL-001")

    st.sidebar.divider()

    product_type = st.sidebar.selectbox(
        "Product Quality",
        options=[0, 1, 2],
        format_func=lambda x: {0: "Low", 1: "Medium", 2: "High"}[x],
        index=1,
    )

    air_temp = st.sidebar.number_input(
        "Room Temperature (°K)",
        min_value=290.0,
        max_value=310.0,
        value=300.0,
        step=0.1,
    )

    process_temp = st.sidebar.number_input(
        "Machine Temperature (°K)",
        min_value=300.0,
        max_value=315.0,
        value=310.0,
        step=0.1,
    )

    rotational_speed = st.sidebar.number_input(
        "Spin Speed (RPM)",
        min_value=1000,
        max_value=3000,
        value=1500,
        step=10,
    )

    torque = st.sidebar.number_input(
        "Twisting Force (Nm)",
        min_value=3.0,
        max_value=80.0,
        value=40.0,
        step=0.1,
    )

    tool_wear = st.sidebar.number_input(
        "Tool Usage (minutes)",
        min_value=0,
        max_value=260,
        value=100,
        step=1,
    )

    # ──────────────────────────────────────────────
    # 4. RUN CHECK BUTTON
    # ──────────────────────────────────────────────
    st.sidebar.divider()
    API_URL = "http://localhost:8000/predict"

    if st.sidebar.button("🚀 Run Check", use_container_width=True):

        payload = {
            "Type": product_type,
            "air_temperature": air_temp,
            "process_temperature": process_temp,
            "rotational_speed": rotational_speed,
            "torque": torque,
            "tool_wear": tool_wear,
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            prediction = result["prediction"]
            probability = result["probability"]
            status = result["status"]

            # Save this check to the audit log
            log_prediction(
                username=st.session_state.username,
                role=st.session_state.role,
                machine_id=component_id,
                inputs=payload,
                result=result,
            )

            # ──────────────────────────────────────
            # 5. SHOW RESULTS
            # ──────────────────────────────────────
            st.subheader("📊 Check Results")

            col1, col2, col3 = st.columns(3)

            col1.metric(label="Result", value="NEEDS REPAIR" if prediction == 1 else "ALL GOOD")
            col2.metric(label="Chance of Breaking Down", value=f"{probability * 100:.2f} %")
            col3.metric(label="Equipment", value=component_id)

            st.divider()

            if prediction == 1:
                st.error(
                    f"🚨 **WARNING — {component_type} ({component_id}) may break down soon!**\n\n"
                    f"There is a **{probability * 100:.2f} %** chance of a breakdown. "
                    "Please alert your supervisor and start the repair process right away.",
                    icon="🔴",
                )
            else:
                st.success(
                    f"✅ **{component_type} ({component_id}) looks fine!**\n\n"
                    f"The chance of breaking down is only **{probability * 100:.2f} %**. "
                    "No action needed — keep running as normal.",
                    icon="🟢",
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "⚠️ Could not connect to the checking system. "
                "Please make sure the server is running and try again."
            )
        except requests.exceptions.HTTPError as http_err:
            st.error(f"⚠️ Something went wrong with the check: {http_err}")
        except Exception as exc:
            st.error(f"⚠️ Unexpected problem: {exc}")

    # ──────────────────────────────────────────────
    # 6. WHAT YOU ENTERED (summary)
    # ──────────────────────────────────────────────
    with st.expander("📋 Current Readings"):
        st.table(
            {
                "Detail": [
                    "Equipment Type",
                    "Equipment ID",
                    "Product Quality",
                    "Room Temperature (°K)",
                    "Machine Temperature (°K)",
                    "Spin Speed (RPM)",
                    "Twisting Force (Nm)",
                    "Tool Usage (minutes)",
                ],
                "Value": [
                    component_type,
                    component_id,
                    {0: "Low", 1: "Medium", 2: "High"}[product_type],
                    air_temp,
                    process_temp,
                    rotational_speed,
                    torque,
                    tool_wear,
                ],
            }
        )
