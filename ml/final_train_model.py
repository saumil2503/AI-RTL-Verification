import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier


# ============================================================
# FINAL AI RTL FAULT DIAGNOSIS MODEL
# ============================================================

print("=" * 75)
print("FINAL AI RTL FAULT DIAGNOSIS MODEL TRAINING")
print("=" * 75)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(
    "dataset/fault_signatures.csv"
)

print("\nDataset:")
print("Samples :", len(df))
print("Columns :", len(df.columns))


# ============================================================
# DEFINE FEATURES
# ============================================================

excluded_columns = [
    "fault_id",
    "window_id",
    "num_vectors"
]

feature_columns = [
    column
    for column in df.columns
    if column not in excluded_columns
]

X = df[feature_columns]
y = df["fault_id"]


print("\nFeature definition:")
print("Total columns :", len(df.columns))
print("Excluded      :", excluded_columns)
print("ML features   :", len(feature_columns))


# ============================================================
# VERIFY FEATURE COUNT
# ============================================================

if len(feature_columns) != 46:

    raise ValueError(
        f"Expected 46 ML features, "
        f"but found {len(feature_columns)}."
    )


# ============================================================
# DISPLAY FEATURES
# ============================================================

print("\nFinal ML features:")

for i, feature in enumerate(
    feature_columns,
    start=1
):
    print(
        f"{i:2d}. {feature}"
    )


# ============================================================
# DISPLAY TARGET DISTRIBUTION
# ============================================================

print("\nTarget distribution:")

print(
    y.value_counts()
    .sort_index()
)


# ============================================================
# TRAIN FINAL RANDOM FOREST
#
# Configuration selected from tuning:
#
# n_estimators = 500
# max_features = None
# random_state = 42
# ============================================================

print("\n")
print("=" * 75)
print("TRAINING FINAL RANDOM FOREST")
print("=" * 75)

model = RandomForestClassifier(
    n_estimators=500,
    max_features=None,
    random_state=42,
    n_jobs=-1
)

print("\nTraining on ALL 192 behavioral signatures...")

model.fit(
    X,
    y
)

print("Training complete.")


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

output_dir = (
    "outputs/final_model"
)

os.makedirs(
    output_dir,
    exist_ok=True
)


# ============================================================
# SAVE MODEL
# ============================================================

model_path = (
    output_dir +
    "/final_random_forest.pkl"
)

joblib.dump(
    model,
    model_path
)


# ============================================================
# SAVE FEATURE LIST
# ============================================================

feature_path = (
    output_dir +
    "/final_feature_list.csv"
)

pd.DataFrame({
    "feature": feature_columns
}).to_csv(
    feature_path,
    index=False
)


# ============================================================
# SAVE MODEL METADATA
# ============================================================

metadata = pd.DataFrame({
    "parameter": [
        "model",
        "n_estimators",
        "max_features",
        "random_state",
        "training_samples",
        "feature_count",
        "fault_classes",
        "behavioral_windows"
    ],

    "value": [
        "Random Forest",
        500,
        "None",
        42,
        len(X),
        len(feature_columns),
        len(y.unique()),
        df["window_id"].nunique()
    ]
})

metadata.to_csv(
    output_dir +
    "/model_metadata.csv",
    index=False
)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

importance_df = pd.DataFrame({
    "feature": feature_columns,
    "importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

importance_df.to_csv(
    output_dir +
    "/final_feature_importance.csv",
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 75)
print("FINAL MODEL GENERATED")
print("=" * 75)

print("\nModel:")
print(
    "Random Forest"
)

print(
    "Trees:",
    model.n_estimators
)

print(
    "Features:",
    len(feature_columns)
)

print(
    "Training samples:",
    len(X)
)

print(
    "Fault classes:",
    len(y.unique())
)

print(
    "Behavioral windows:",
    df["window_id"].nunique()
)

print("\nGenerated files:")

print(
    " -",
    model_path
)

print(
    " -",
    feature_path
)

print(
    " -",
    output_dir +
    "/model_metadata.csv"
)

print(
    " -",
    output_dir +
    "/final_feature_importance.csv"
)

print("\n")
print("=" * 75)
print("FINAL MODEL TRAINING COMPLETE")
print("=" * 75)