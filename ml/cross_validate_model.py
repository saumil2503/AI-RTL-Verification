import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import GroupKFold


# ============================================================
# 4-FOLD GROUP CROSS-VALIDATION
# AI RTL FAULT DIAGNOSIS
# ============================================================

print("=" * 75)
print("4-FOLD GROUP CROSS-VALIDATION")
print("=" * 75)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv("dataset/fault_signatures.csv")


print("\nDataset:")
print("Samples :", len(df))
print("Columns :", len(df.columns))


# ============================================================
# TARGET
# ============================================================

TARGET = "fault_id"


# ============================================================
# NON-ML COLUMNS
#
# fault_id  -> target
# window_id -> grouping information
# num_vectors -> metadata, not a predictive feature
# ============================================================

NON_FEATURE_COLUMNS = [
    "fault_id",
    "window_id",
    "num_vectors"
]


# ============================================================
# EXACT 46 ML FEATURES
# ============================================================

FEATURE_COLUMNS = [
    column
    for column in df.columns
    if column not in NON_FEATURE_COLUMNS
]


print("\nFeature definition:")
print("Total dataset columns :", len(df.columns))
print("ML features            :", len(FEATURE_COLUMNS))

print("\nML feature columns:")

for feature in FEATURE_COLUMNS:
    print(" -", feature)


# ============================================================
# SAFETY CHECK
# ============================================================

if len(FEATURE_COLUMNS) != 46:

    raise ValueError(
        f"Expected exactly 46 ML features, "
        f"but found {len(FEATURE_COLUMNS)}."
    )


# ============================================================
# FEATURE MATRIX
# ============================================================

X = df[FEATURE_COLUMNS].copy()

y = df[TARGET].copy()

groups = df["window_id"].copy()


print("\nFeature matrix:")
print("Samples :", len(X))
print("Features:", X.shape[1])

print("\nFault classes:")
print(sorted(y.unique()))

print("\nGroups:")
print("Number of behavioral windows:",
      groups.nunique())


# ============================================================
# GROUP K-FOLD
#
# Entire behavioral windows stay together.
#
# 32 windows / fault
# 32 total window IDs
#
# 4 folds:
#
# 8 windows testing
# 24 windows training
# ============================================================

group_kfold = GroupKFold(n_splits=4)


fold_accuracies = []

all_actual = []
all_predicted = []


# ============================================================
# FOLD LOOP
# ============================================================

for fold_number, (train_index, test_index) in enumerate(
        group_kfold.split(X, y, groups=groups),
        start=1):


    print("\n" + "=" * 75)
    print(f"FOLD {fold_number}")
    print("=" * 75)


    X_train = X.iloc[train_index]
    X_test = X.iloc[test_index]

    y_train = y.iloc[train_index]
    y_test = y.iloc[test_index]

    train_groups = groups.iloc[train_index]
    test_groups = groups.iloc[test_index]


    print("\nTest windows:",
          sorted(test_groups.unique()))

    print("Training samples:",
          len(X_train))

    print("Testing samples :",
          len(X_test))


    # ========================================================
    # RANDOM FOREST
    # ========================================================

    model = RandomForestClassifier(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    )


    print("\nTraining Random Forest...")

    model.fit(
        X_train,
        y_train
    )

    print("Training complete.")


    # ========================================================
    # PREDICTION
    # ========================================================

    predictions = model.predict(X_test)


    # ========================================================
    # ACCURACY
    # ========================================================

    accuracy = accuracy_score(
        y_test,
        predictions
    )


    fold_accuracies.append(accuracy)


    print(
        f"\nFold {fold_number} accuracy: "
        f"{accuracy * 100:.2f}%"
    )


    # ========================================================
    # CONFUSION MATRIX
    # ========================================================

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=[1, 2, 3, 4, 5, 6]
    )


    print("\nConfusion Matrix:")
    print(cm)


    # ========================================================
    # STORE PREDICTIONS
    # ========================================================

    all_actual.extend(
        y_test.tolist()
    )

    all_predicted.extend(
        predictions.tolist()
    )


# ============================================================
# CROSS-VALIDATION SUMMARY
# ============================================================

mean_accuracy = np.mean(
    fold_accuracies
)

std_accuracy = np.std(
    fold_accuracies
)


print("\n" + "=" * 75)
print("CROSS-VALIDATION SUMMARY")
print("=" * 75)


for index, accuracy in enumerate(
        fold_accuracies,
        start=1):

    print(
        f"Fold {index}: "
        f"{accuracy * 100:.2f}%"
    )


print(
    f"\nMean Accuracy: "
    f"{mean_accuracy * 100:.2f}%"
)


print(
    f"Standard Deviation: "
    f"{std_accuracy * 100:.2f}%"
)


# ============================================================
# OVERALL PREDICTION COUNT
# ============================================================

overall_accuracy = accuracy_score(
    all_actual,
    all_predicted
)


print(
    f"\nOverall Accuracy: "
    f"{overall_accuracy * 100:.2f}%"
)


# ============================================================
# FINAL INTERPRETATION
# ============================================================

print("\n" + "=" * 75)
print("FINAL INTERPRETATION")
print("=" * 75)

print("""
The Random Forest was evaluated using four
group-based folds.

The following columns were excluded from the
ML feature matrix:

    fault_id
    window_id
    num_vectors

Exactly 46 behavioral features were used.

Entire behavioral windows were kept together
during validation so that samples from the same
window were not mixed between training and testing.

This provides a stronger estimate of the model's
ability to generalize to unseen behavioral windows.
""")


print("=" * 75)
print("4-FOLD GROUP CROSS-VALIDATION COMPLETE")
print("=" * 75)