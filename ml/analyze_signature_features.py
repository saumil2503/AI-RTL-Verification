import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier


# ============================================================
# BEHAVIORAL FAULT SIGNATURE
# FEATURE IMPORTANCE ANALYSIS
# ============================================================

INPUT_FILE = "dataset/fault_signatures.csv"


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)


print("=" * 75)
print("FAULT SIGNATURE FEATURE IMPORTANCE")
print("=" * 75)


# ============================================================
# 2. SEPARATE FEATURES AND TARGET
# ============================================================

X = df.drop(
    columns=[
        "fault_id",
        "window_id",
        "num_vectors"
    ]
)

y = df["fault_id"]


print("\nSamples :", len(X))
print("Features:", len(X.columns))


# ============================================================
# 3. TRAIN RANDOM FOREST
# ============================================================

model = RandomForestClassifier(
    n_estimators=500,
    random_state=42,
    n_jobs=-1
)


print("\nTraining Random Forest...")

model.fit(
    X,
    y
)

print("Training complete.")


# ============================================================
# 4. FEATURE IMPORTANCE
# ============================================================

importance = pd.DataFrame({

    "Feature":
        X.columns,

    "Importance":
        model.feature_importances_

})


importance = importance.sort_values(
    "Importance",
    ascending=False
).reset_index(
    drop=True
)


# ============================================================
# 5. DISPLAY TOP FEATURES
# ============================================================

print("\n" + "=" * 75)
print("TOP 20 FEATURES")
print("=" * 75)

print(
    importance.head(20)
    .to_string(index=False)
)


# ============================================================
# 6. SAVE RESULTS
# ============================================================

importance.to_csv(
    "outputs/signature_models/feature_importance.csv",
    index=False
)


# ============================================================
# 7. SAVE TOP 10
# ============================================================

print("\nTop 10 behavioral features:")

for index, row in importance.head(10).iterrows():

    print(
        f"{index + 1:2d}. "
        f"{row['Feature']:<35} "
        f"{row['Importance']:.6f}"
    )


# ============================================================
# 8. FINAL
# ============================================================

print("\n" + "=" * 75)
print("FEATURE IMPORTANCE ANALYSIS COMPLETE")
print("=" * 75)

print(
    "\nGenerated:"
)

print(
    " - outputs/signature_models/feature_importance.csv"
)

print("=" * 75)