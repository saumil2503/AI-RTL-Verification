import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import confusion_matrix


# ============================================================
# MISCLASSIFIED WINDOW ANALYSIS
# ============================================================

print("=" * 75)
print("MISCLASSIFIED BEHAVIORAL WINDOW ANALYSIS")
print("=" * 75)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    "dataset/fault_signatures.csv"
)


# ============================================================
# FEATURES
# ============================================================

NON_FEATURE_COLUMNS = [
    "fault_id",
    "window_id",
    "num_vectors"
]

FEATURE_COLUMNS = [
    c for c in df.columns
    if c not in NON_FEATURE_COLUMNS
]


X = df[FEATURE_COLUMNS]

y = df["fault_id"]

groups = df["window_id"]


print("\nDataset:")
print("Samples :", len(df))
print("Features:", len(FEATURE_COLUMNS))
print("Windows :", groups.nunique())


# ============================================================
# GROUP CROSS VALIDATION
# ============================================================

gkf = GroupKFold(
    n_splits=4
)


all_results = []


fold_number = 1


for train_idx, test_idx in gkf.split(
    X,
    y,
    groups
):

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    test_df = df.iloc[test_idx].copy()


    print("\n" + "=" * 75)
    print(f"FOLD {fold_number}")
    print("=" * 75)


    print(
        "Test windows:",
        sorted(
            test_df["window_id"].unique()
        )
    )


    # ========================================================
    # TRAIN
    # ========================================================

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
        max_features="sqrt",
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

    predictions = model.predict(
        X_test
    )


    test_df["predicted_fault"] = predictions


    test_df["correct"] = (
        test_df["fault_id"]
        ==
        test_df["predicted_fault"]
    )


    accuracy = (
        test_df["correct"].mean()
        *
        100
    )


    print(
        f"\nFold accuracy: "
        f"{accuracy:.2f}%"
    )


    # ========================================================
    # CONFUSION MATRIX
    # ========================================================

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=sorted(y.unique())
    )


    print("\nConfusion Matrix:")
    print(cm)


    # ========================================================
    # MISCLASSIFICATIONS
    # ========================================================

    wrong = test_df[
        ~test_df["correct"]
    ]


    if len(wrong) == 0:

        print(
            "\nNo misclassified windows."
        )

    else:

        print(
            "\nMisclassified samples:"
        )


        summary = (
            wrong
            .groupby(
                [
                    "fault_id",
                    "predicted_fault"
                ]
            )
            .size()
            .reset_index(
                name="count"
            )
        )


        print(
            summary.to_string(
                index=False
            )
        )


        print(
            "\nMisclassified window IDs:"
        )


        window_summary = (
            wrong
            .groupby(
                [
                    "window_id",
                    "fault_id",
                    "predicted_fault"
                ]
            )
            .size()
            .reset_index(
                name="samples"
            )
        )


        print(
            window_summary.to_string(
                index=False
            )
        )


        # Save for later analysis

        output_file = (
            "outputs/signature_models/"
            f"fold_{fold_number}_misclassified.csv"
        )


        wrong.to_csv(
            output_file,
            index=False
        )


        print(
            f"\nSaved:"
            f"\n - {output_file}"
        )


        all_results.append(
            wrong
        )


    fold_number += 1


# ============================================================
# COMBINE ALL MISCLASSIFICATIONS
# ============================================================

print("\n" + "=" * 75)
print("GLOBAL MISCLASSIFICATION SUMMARY")
print("=" * 75)


if all_results:

    all_wrong = pd.concat(
        all_results,
        ignore_index=True
    )


    print(
        "\nTotal misclassified samples:",
        len(all_wrong)
    )


    global_summary = (
        all_wrong
        .groupby(
            [
                "fault_id",
                "predicted_fault"
            ]
        )
        .size()
        .reset_index(
            name="count"
        )
        .sort_values(
            "count",
            ascending=False
        )
    )


    print(
        "\nMost common wrong predictions:"
    )


    print(
        global_summary.to_string(
            index=False
        )
    )


    global_summary.to_csv(
        "outputs/signature_models/"
        "global_misclassification_summary.csv",
        index=False
    )


    print(
        "\nGenerated:"
        "\n - outputs/signature_models/"
        "global_misclassification_summary.csv"
    )


else:

    print(
        "\nNo misclassifications found."
    )


print("\n" + "=" * 75)
print("MISCLASSIFICATION ANALYSIS COMPLETE")
print("=" * 75)