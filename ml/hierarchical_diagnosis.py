import os
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import accuracy_score, confusion_matrix


# ============================================================
# HIERARCHICAL AI RTL FAULT DIAGNOSIS
#
# Stage 1:
#   Global Random Forest
#
# Stage 2:
#   Specialist classifiers for difficult fault pairs
#
# Difficult pairs discovered from previous analysis:
#   Fault 2 vs Fault 6
#   Fault 4 vs Fault 1
#   Fault 4 vs Fault 5
# ============================================================


print("=" * 75)
print("HIERARCHICAL AI RTL FAULT DIAGNOSIS")
print("=" * 75)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv("dataset/fault_signatures.csv")

print("\nDataset:")
print("Samples :", len(df))
print("Columns :", len(df.columns))


# ============================================================
# FEATURE DEFINITION
# ============================================================

excluded = [
    "fault_id",
    "window_id",
    "num_vectors"
]

features = [
    column
    for column in df.columns
    if column not in excluded
]

X = df[features]
y = df["fault_id"]
groups = df["window_id"]


print("\nFeature definition:")
print("Total columns :", len(df.columns))
print("ML features   :", len(features))

print("\nFeature matrix:")
print("Samples :", len(X))
print("Features:", len(features))

print("\nFault classes:")
print(sorted(y.unique()))

print("\nBehavioral windows:")
print(groups.nunique())


# ============================================================
# SPECIALIST PAIRS
# ============================================================

SPECIALIST_PAIRS = [
    (2, 6),
    (4, 1),
    (4, 5)
]


# ============================================================
# FUNCTION:
# TRAIN SPECIALIST
# ============================================================

def train_specialist(X_train, y_train, fault_a, fault_b):

    mask = (
        (y_train == fault_a) |
        (y_train == fault_b)
    )

    X_pair = X_train.loc[mask]
    y_pair = y_train.loc[mask]

    model = RandomForestClassifier(
        n_estimators=500,
        max_features=None,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_pair, y_pair)

    return model


# ============================================================
# FUNCTION:
# HIERARCHICAL PREDICTION
# ============================================================

def hierarchical_predict(
    global_model,
    specialist_models,
    X_test
):

    global_prediction = global_model.predict(X_test)

    final_prediction = global_prediction.copy()

    for pair, specialist in specialist_models.items():

        fault_a, fault_b = pair

        mask = (
            (global_prediction == fault_a) |
            (global_prediction == fault_b)
        )

        if np.any(mask):

            specialist_prediction = specialist.predict(
                X_test.loc[mask]
            )

            final_prediction[mask] = specialist_prediction

    return final_prediction


# ============================================================
# GROUP CROSS VALIDATION
# ============================================================

gkf = GroupKFold(n_splits=4)

fold_results = []

all_actual = []
all_predicted = []


print("\n")
print("=" * 75)
print("4-FOLD HIERARCHICAL GROUP CROSS-VALIDATION")
print("=" * 75)


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

    print("\n")
    print("=" * 75)
    print("FOLD", fold)
    print("=" * 75)

    print("Test windows:", test_windows)
    print("Training samples:", len(train_idx))
    print("Testing samples :", len(test_idx))


    # ========================================================
    # STAGE 1
    # GLOBAL RANDOM FOREST
    # ========================================================

    print("\nTraining Global Random Forest...")

    global_model = RandomForestClassifier(
        n_estimators=500,
        max_features=None,
        random_state=42,
        n_jobs=-1
    )

    global_model.fit(
        X_train,
        y_train
    )

    print("Global model trained.")


    # ========================================================
    # GLOBAL PREDICTION
    # ========================================================

    global_prediction = global_model.predict(
        X_test
    )

    global_accuracy = accuracy_score(
        y_test,
        global_prediction
    )


    print(
        f"\nGlobal RF accuracy: "
        f"{global_accuracy * 100:.2f}%"
    )


    # ========================================================
    # STAGE 2
    # SPECIALIST MODELS
    # ========================================================

    print("\nTraining specialist models...")

    specialist_models = {}

    for pair in SPECIALIST_PAIRS:

        fault_a, fault_b = pair

        print(
            f"  Specialist: Fault #{fault_a} "
            f"vs Fault #{fault_b}"
        )

        specialist_models[pair] = train_specialist(
            X_train,
            y_train,
            fault_a,
            fault_b
        )


    print("Specialist models trained.")


    # ========================================================
    # HIERARCHICAL PREDICTION
    # ========================================================

    hierarchical_prediction = hierarchical_predict(
        global_model,
        specialist_models,
        X_test
    )


    hierarchical_accuracy = accuracy_score(
        y_test,
        hierarchical_prediction
    )


    print(
        f"\nHierarchical accuracy: "
        f"{hierarchical_accuracy * 100:.2f}%"
    )


    improvement = (
        hierarchical_accuracy -
        global_accuracy
    ) * 100


    print(
        f"Improvement over Global RF: "
        f"{improvement:+.2f}%"
    )


    # ========================================================
    # CONFUSION MATRIX
    # ========================================================

    cm = confusion_matrix(
        y_test,
        hierarchical_prediction,
        labels=[1, 2, 3, 4, 5, 6]
    )

    print("\nHierarchical Confusion Matrix:")

    print(cm)


    # ========================================================
    # STORE RESULTS
    # ========================================================

    fold_results.append({
        "Fold": fold,
        "Global_RF": global_accuracy,
        "Hierarchical": hierarchical_accuracy,
        "Improvement": improvement / 100
    })


    all_actual.extend(
        y_test.tolist()
    )

    all_predicted.extend(
        hierarchical_prediction.tolist()
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

results_df = pd.DataFrame(
    fold_results
)


print("\n")
print("=" * 75)
print("HIERARCHICAL MODEL SUMMARY")
print("=" * 75)


for _, row in results_df.iterrows():

    print(
        f"Fold {int(row['Fold'])}: "
        f"Global RF = "
        f"{row['Global_RF'] * 100:.2f}%   |   "
        f"Hierarchical = "
        f"{row['Hierarchical'] * 100:.2f}%   |   "
        f"Improvement = "
        f"{row['Improvement'] * 100:+.2f}%"
    )


global_mean = results_df[
    "Global_RF"
].mean()

hierarchical_mean = results_df[
    "Hierarchical"
].mean()

hierarchical_std = results_df[
    "Hierarchical"
].std()

improvement_mean = (
    hierarchical_mean -
    global_mean
)


print("\n")
print("=" * 75)
print("FINAL RESULTS")
print("=" * 75)


print(
    f"\nGlobal RF Mean Accuracy:"
    f" {global_mean * 100:.2f}%"
)

print(
    f"Hierarchical Mean Accuracy:"
    f" {hierarchical_mean * 100:.2f}%"
)

print(
    f"Hierarchical Std Deviation:"
    f" {hierarchical_std * 100:.2f}%"
)

print(
    f"Average Improvement:"
    f" {improvement_mean * 100:+.2f}%"
)


# ============================================================
# OVERALL CONFUSION MATRIX
# ============================================================

overall_cm = confusion_matrix(
    all_actual,
    all_predicted,
    labels=[1, 2, 3, 4, 5, 6]
)


print("\n")
print("=" * 75)
print("OVERALL HIERARCHICAL CONFUSION MATRIX")
print("=" * 75)

print(overall_cm)


# ============================================================
# FAULT-WISE ACCURACY
# ============================================================

print("\n")
print("=" * 75)
print("FAULT-WISE HIERARCHICAL ACCURACY")
print("=" * 75)


all_actual_np = np.array(
    all_actual
)

all_predicted_np = np.array(
    all_predicted
)


for fault in [1, 2, 3, 4, 5, 6]:

    mask = (
        all_actual_np == fault
    )

    total = np.sum(mask)

    correct = np.sum(
        all_predicted_np[mask] == fault
    )

    accuracy = (
        correct / total
        if total > 0
        else 0
    )

    print(
        f"Fault #{fault}: "
        f"{correct}/{total} "
        f"({accuracy * 100:.2f}%)"
    )


# ============================================================
# SAVE RESULTS
# ============================================================

os.makedirs(
    "outputs/signature_models",
    exist_ok=True
)


results_df.to_csv(
    "outputs/signature_models/"
    "hierarchical_cv_results.csv",
    index=False
)


pd.DataFrame(
    overall_cm,
    index=[
        "Actual_1",
        "Actual_2",
        "Actual_3",
        "Actual_4",
        "Actual_5",
        "Actual_6"
    ],
    columns=[
        "Pred_1",
        "Pred_2",
        "Pred_3",
        "Pred_4",
        "Pred_5",
        "Pred_6"
    ]
).to_csv(
    "outputs/signature_models/"
    "hierarchical_confusion_matrix.csv"
)


# ============================================================
# FINAL DECISION
# ============================================================

print("\n")
print("=" * 75)
print("FINAL MODEL DECISION")
print("=" * 75)


if hierarchical_mean > 0.8958:

    print(
        "\nRESULT:"
    )

    print(
        "HIERARCHICAL MODEL BEATS "
        "THE 89.58% RANDOM FOREST BASELINE."
    )

    print(
        "Recommended: USE HIERARCHICAL MODEL."
    )

elif hierarchical_mean > global_mean:

    print(
        "\nRESULT:"
    )

    print(
        "Hierarchical model improves over "
        "the global RF, but does not exceed "
        "the tuned 89.58% baseline."
    )

    print(
        "Further architecture analysis may "
        "be required."
    )

else:

    print(
        "\nRESULT:"
    )

    print(
        "Hierarchical model does not improve "
        "over the global RF."
    )

    print(
        "Keep the tuned Random Forest baseline."
    )


print("\n")
print("=" * 75)
print("HIERARCHICAL DIAGNOSIS COMPLETE")
print("=" * 75)

print("\nGenerated:")
print(
    " - outputs/signature_models/"
    "hierarchical_cv_results.csv"
)

print(
    " - outputs/signature_models/"
    "hierarchical_confusion_matrix.csv"
)
