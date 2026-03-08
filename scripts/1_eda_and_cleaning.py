# %% [markdown]
# # Phase 1 — EDA & Data Cleaning
# Predictive Maintenance Early-Warning System
# This script loads the raw sensor data, removes non-predictive columns,
# encodes categoricals, splits into train/test, and saves processed CSVs.

# %%
# ──────────────────────────────────────────────
# 1. IMPORTS
# ──────────────────────────────────────────────
import os
import pandas as pd
from sklearn.model_selection import train_test_split

# %%
# ──────────────────────────────────────────────
# 2. LOAD RAW DATA
# ──────────────────────────────────────────────
# Read the raw CSV that ships with the repo.
# We use a path relative to the script location so it works regardless of CWD.
raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw_data.csv")
df = pd.read_csv(raw_path)

# Quick sanity check — shape & first few rows
print(f"Raw data shape: {df.shape}")
print(df.head())

# %%
# ──────────────────────────────────────────────
# 3. INSPECT COLUMNS & TYPES
# ──────────────────────────────────────────────
# Useful to confirm column names and spot nulls before we start cleaning.
print("\n--- Column dtypes ---")
print(df.dtypes)

print("\n--- Missing values per column ---")
print(df.isnull().sum())

print("\n--- Basic statistics ---")
print(df.describe())

# %%
# ──────────────────────────────────────────────
# 4. DROP USELESS IDENTIFIER COLUMNS
# ──────────────────────────────────────────────
# 'UDI' and 'Product ID' are row identifiers — they carry zero predictive
# signal and would only introduce noise or cause the model to memorise IDs.
cols_to_drop = ["UDI", "Product ID"]
df.drop(columns=cols_to_drop, inplace=True)

print(f"\nDropped {cols_to_drop}. New shape: {df.shape}")

# Rename columns to remove brackets — XGBoost rejects [, ], and < in
# feature names.  Clean snake_case names also make the API simpler.
df.rename(columns={
    "Air temperature [K]": "Air_temperature_K",
    "Process temperature [K]": "Process_temperature_K",
    "Rotational speed [rpm]": "Rotational_speed_rpm",
    "Torque [Nm]": "Torque_Nm",
    "Tool wear [min]": "Tool_wear_min",
}, inplace=True)

print(f"Renamed columns: {list(df.columns)}")

# %%
# ──────────────────────────────────────────────
# 5. ENCODE THE 'Type' CATEGORICAL
# ──────────────────────────────────────────────
# 'Type' has three quality tiers: L (Low), M (Medium), H (High).
# We map them to ordinal integers so tree-based models can consume them
# directly without one-hot encoding.
type_mapping = {"L": 0, "M": 1, "H": 2}
df["Type"] = df["Type"].map(type_mapping)

print("\nType column after mapping:")
print(df["Type"].value_counts().sort_index())

# %%
# ──────────────────────────────────────────────
# 6. DEFINE TARGET & DROP LEAKAGE COLUMNS
# ──────────────────────────────────────────────
# 'Machine failure' is the binary target we want to predict (0 = healthy,
# 1 = failure).
#
# The five failure-mode columns (TWF, HDF, PWF, OSF, RNF) describe *how*
# the machine failed.  Including them as features would leak the answer to
# the model — if any of these is 1, the target is trivially 1.
# We must remove them from the feature set.

target_col = "Machine failure"
failure_mode_cols = ["TWF", "HDF", "PWF", "OSF", "RNF"]

# Isolate y (target vector)
y = df[target_col]

# Build X by dropping the target AND the failure-mode leakage columns
X = df.drop(columns=[target_col] + failure_mode_cols)

print(f"\nFeatures  (X) shape: {X.shape}  — columns: {list(X.columns)}")
print(f"Target    (y) shape: {y.shape}  — distribution:\n{y.value_counts()}")

# %%
# ──────────────────────────────────────────────
# 7. TRAIN / TEST SPLIT  (80 / 20)
# ──────────────────────────────────────────────
# stratify=y keeps the failure-class ratio consistent across both splits,
# which is important because the dataset is heavily imbalanced.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"\nX_train: {X_train.shape}   X_test: {X_test.shape}")
print(f"y_train distribution:\n{y_train.value_counts()}")
print(f"y_test  distribution:\n{y_test.value_counts()}")

# %%
# ──────────────────────────────────────────────
# 8. SAVE PROCESSED DATA TO data/processed/
# ──────────────────────────────────────────────
# Create the output directory if it doesn't already exist.
processed_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(processed_dir, exist_ok=True)

# Save each split as its own CSV so Phase 2 can load them independently.
# index=False avoids writing the pandas index as an extra column.
X_train.to_csv(os.path.join(processed_dir, "X_train.csv"), index=False)
X_test.to_csv(os.path.join(processed_dir, "X_test.csv"), index=False)
y_train.to_csv(os.path.join(processed_dir, "y_train.csv"), index=False)
y_test.to_csv(os.path.join(processed_dir, "y_test.csv"), index=False)

print(f"\n✓ Processed files saved to {os.path.abspath(processed_dir)}")
print("  ├── X_train.csv")
print("  ├── X_test.csv")
print("  ├── y_train.csv")
print("  └── y_test.csv")
print("\nPhase 1 complete. Ready for Phase 2: Model Training.")