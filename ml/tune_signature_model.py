import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import accuracy_score, confusion_matrix

# ============================================================
# AI RTL FAULT DIAGNOSIS
# RANDOM FOREST HYPERPARAMETER TUNING
# ============================================================

print("=" * 75)
print("RANDOM FOREST HYPERPARAMETER TUNING")
print("=" * 75)

# ------------------------------------------------------------
# LOAD DATASET
# ------------------------------------------------------------

df = pd.read_csv("dataset/fault_signatures.csv")

print("\nDataset:")
print("Samples :", len(df))
print("Columns :", len(df.columns))

# ------------------------------------------------------------
# FEATURE DEFINITION
# ------------------------------------------------------------

excluded = [
    "fault_id",
    "window_id",
    "num_vectors"
]

feature_columns = [
    c for c in df.columns
    if c not in excluded
]

X = df[feature_columns]
y = df["fault_id"]
groups = df["window_id"]

print("\nFeature definition:")
print("Total dataset columns :", len(df.columns))
print("ML features            :", len(feature_columns))

print("\nFeature matrix:")
print("Samples :", len(X))
print("Features:", len(feature_columns))

print("\nFault classes:")
print(sorted(y.unique()))

print("\nBehavioral windows:")
print(groups.nunique())

# ------------------------------------------------------------
# MODELS TO TEST
# ------------------------------------------------------------

models = {

    "RF_500_sqrt": RandomForestClassifier(
        n_estimators=500,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    ),

    "RF_1000_sqrt": RandomForestClassifier(
        n_estimators=1000,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    ),

    "RF_500_log2": RandomForestClassifier(
        n_estimators=500,
        max_features="log2",
        random_state=42,
        n_jobs=-1
    ),

    "RF_500_all": RandomForestClassifier(
        n_estimators=500,
        max_features=None,
        random_state=42,
        n_jobs=-1
    ),

    "RF_500_balanced": RandomForestClassifier(
        n_estimators=500,
        max_features="sqrt",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "RF_1000_balanced": RandomForestClassifier(
        n_estimators=1000,
        max_features="sqrt",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
}

# ------------------------------------------------------------
# GROUP K-FOLD
# ------------------------------------------------------------

gkf = GroupKFold(n_splits=4)

results = []

# ------------------------------------------------------------
# RUN EXPERIMENTS
# ------------------------------------------------------------

for model_name, model in models.items():

    print("\n")
    print("=" * 75)
    print("MODEL:", model_name)
    print("=" * 75)

    fold_scores = []

    for fold, (train_idx, test_idx) in enumerate(
        gkf.split(X, y, groups),
        start=1
    ):

        X_train = X.iloc[train_idx]
        X_test = X.iloc[test_idx]

        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        test_windows = sorted(
            groups.iloc[test_idx].unique()
        )

        print("\nFold", fold)
        print("Test windows:", test_windows)
        print("Training samples:", len(train_idx))
        print("Testing samples :", len(test_idx))

        print("Training...")

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        fold_scores.append(accuracy)

        print(
            f"Fold {fold} accuracy: "
            f"{accuracy * 100:.2f}%"
        )

    mean_accuracy = np.mean(fold_scores)
    std_accuracy = np.std(fold_scores)

    print("\n------------------------------------------")
    print("MODEL SUMMARY")
    print("------------------------------------------")

    print(
        "Fold scores:",
        [
            f"{score * 100:.2f}%"
            for score in fold_scores
        ]
    )

    print(
        f"Mean Accuracy: "
        f"{mean_accuracy * 100:.2f}%"
    )

    print(
        f"Std Deviation: "
        f"{std_accuracy * 100:.2f}%"
    )

    results.append({
        "Model": model_name,
        "Fold_1": fold_scores[0],
        "Fold_2": fold_scores[1],
        "Fold_3": fold_scores[2],
        "Fold_4": fold_scores[3],
        "Mean_Accuracy": mean_accuracy,
        "Std_Deviation": std_accuracy
    })

# ------------------------------------------------------------
# RESULTS TABLE
# ------------------------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Mean_Accuracy",
    ascending=False
)

print("\n")
print("=" * 75)
print("FINAL RANDOM FOREST COMPARISON")
print("=" * 75)

display_df = results_df.copy()

display_df["Mean_Accuracy"] = (
    display_df["Mean_Accuracy"] * 100
)

display_df["Std_Deviation"] = (
    display_df["Std_Deviation"] * 100
)

for column in [
    "Fold_1",
    "Fold_2",
    "Fold_3",
    "Fold_4"
]:
    display_df[column] = (
        display_df[column] * 100
    )

print(
    display_df.to_string(
        index=False,
        formatters={
            "Fold_1": "{:.2f}%".format,
            "Fold_2": "{:.2f}%".format,
            "Fold_3": "{:.2f}%".format,
            "Fold_4": "{:.2f}%".format,
            "Mean_Accuracy": "{:.2f}%".format,
            "Std_Deviation": "{:.2f}%".format
        }
    )
)

# ------------------------------------------------------------
# BEST MODEL
# ------------------------------------------------------------

best_row = results_df.iloc[0]

print("\n")
print("=" * 75)
print("BEST MODEL")
print("=" * 75)

print("Model :", best_row["Model"])

print(
    f"Mean Accuracy : "
    f"{best_row['Mean_Accuracy'] * 100:.2f}%"
)

print(
    f"Std Deviation : "
    f"{best_row['Std_Deviation'] * 100:.2f}%"
)

# ------------------------------------------------------------
# SAVE RESULTS
# ------------------------------------------------------------

import os

os.makedirs(
    "outputs/signature_models",
    exist_ok=True
)

results_df.to_csv(
    "outputs/signature_models/"
    "random_forest_tuning_results.csv",
    index=False
)

print("\nGenerated:")
print(
    " - outputs/signature_models/"
    "random_forest_tuning_results.csv"
)

print("\n")
print("=" * 75)
print("RANDOM FOREST TUNING COMPLETE")
print("=" * 75)