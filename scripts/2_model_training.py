# %% [markdown]
# # Phase 2 — Model Training & Evaluation
# Predictive Maintenance Early-Warning System
# This script loads the processed train/test splits from Phase 1,
# trains a Random Forest classifier tuned for class imbalance, evaluates it
# with recall-focused metrics, and saves the model artifact for the API.

# %%
# ──────────────────────────────────────────────
# 1. IMPORTS
# ──────────────────────────────────────────────
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# %%
# ──────────────────────────────────────────────
# 2. LOAD PROCESSED DATA FROM PHASE 1
# ──────────────────────────────────────────────
# All paths are relative to this script's location so the code runs
# regardless of the working directory VS Code happens to use.
data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

X_train = pd.read_csv(os.path.join(data_dir, "X_train.csv"))
X_test  = pd.read_csv(os.path.join(data_dir, "X_test.csv"))
y_train = pd.read_csv(os.path.join(data_dir, "y_train.csv")).squeeze()   # squeeze → Series
y_test  = pd.read_csv(os.path.join(data_dir, "y_test.csv")).squeeze()

print(f"X_train: {X_train.shape}   X_test: {X_test.shape}")
print(f"Features: {list(X_train.columns)}")
print(f"\ny_train distribution:\n{y_train.value_counts()}")

# %%
# ──────────────────────────────────────────────
# 3. COMPUTE CLASS WEIGHT FOR IMBALANCE
# ──────────────────────────────────────────────
# Machine failures are rare events (~3 % of the dataset).
# We can use class_weight="balanced" in Random Forest to automatically
# adjust weights inversely proportional to class frequencies.
neg_count = (y_train == 0).sum()
pos_count = (y_train == 1).sum()

print(f"\nNegative samples: {neg_count}   Positive samples: {pos_count}")
print(f"Using class_weight='balanced' in Random Forest")

# %%
# ──────────────────────────────────────────────
# 4. INITIALISE RANDOM FOREST CLASSIFIER
# ──────────────────────────────────────────────
# Key hyper-parameters explained:
#   n_estimators    — number of trees in the forest.
#   max_depth       — maximum tree depth; keeps complexity in check.
#   class_weight    — compensates for heavy class imbalance automatically.
#   random_state    — reproducibility.
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    class_weight="balanced",
    random_state=42,
)

print("\nModel initialised:")
print(model)

# %%
# ──────────────────────────────────────────────
# 5. TRAIN THE MODEL
# ──────────────────────────────────────────────
model.fit(X_train, y_train)

print("\n✓ Training complete.")

# %%
# ──────────────────────────────────────────────
# 6. EVALUATE ON THE TEST SET
# ──────────────────────────────────────────────
# Generate predictions on the held-out test split.
y_pred = model.predict(X_test)

# --- Confusion Matrix ---
# Layout:
#            Predicted 0   Predicted 1
# Actual 0     TN            FP
# Actual 1     FN            TP
#
# For an early-warning system we care most about minimising FN (bottom-left)
# because a missed failure (False Negative) means the factory doesn't get
# an alert and a machine breaks down unexpectedly.
print("\n--- CONFUSION MATRIX ---")
print(confusion_matrix(y_test, y_pred))

# --- Classification Report ---
# RECALL is the single most important metric here.
# Recall = TP / (TP + FN)
# A high recall means we catch almost every real failure, even if it means
# a few extra false alarms (lower precision).  In predictive maintenance
# the cost of a missed failure far outweighs the cost of a false alert.
print("\n--- CLASSIFICATION REPORT ---")
print(classification_report(y_test, y_pred, target_names=["Healthy", "Failure"]))

# %%
# ──────────────────────────────────────────────
# 7. SAVE THE TRAINED MODEL (THE HANDOFF)
# ──────────────────────────────────────────────
# The API in Phase 3 will load this .pkl file at startup to serve
# real-time predictions over HTTP.
models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(models_dir, exist_ok=True)

model_path = os.path.join(models_dir, "random_forest_model.pkl")
joblib.dump(model, model_path)

print(f"\n✓ Model saved to {os.path.abspath(model_path)}")
print("\nPhase 2 complete. Ready for Phase 3: FastAPI Backend.")
