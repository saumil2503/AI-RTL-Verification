import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import matplotlib.pyplot as plt


# ============================================================
# AI-ASSISTED RTL VERIFICATION & BUG DIAGNOSIS
#
# BEHAVIORAL FAULT SIGNATURE ML
# ============================================================

INPUT_FILE = "dataset/fault_signatures.csv"

os.makedirs("outputs/signature_models", exist_ok=True)


# ============================================================
# 1. LOAD SIGNATURE DATASET
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 75)
print("BEHAVIORAL FAULT SIGNATURE ML")
print("=" * 75)

print("\nDataset:")
print("Rows    :", len(df))
print("Columns :", len(df.columns))


# ============================================================
# 2. REMOVE IDENTIFICATION COLUMNS
# ============================================================
#
# fault_id = target
#
# window_id is NOT a behavioral feature.
# It only tells us which window number it is.
#
# num_vectors is constant (=32), so it contains no useful
# classification information either.
# ============================================================

X = df.drop(
    columns=[
        "fault_id",
        "window_id",
        "num_vectors"
    ]
)

y = df["fault_id"]


print("\nML feature matrix:")
print("Samples :", len(X))
print("Features:", X.shape[1])

print("\nFault classes:")
print(sorted(y.unique()))


# ============================================================
# 3. STRATIFIED TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nDataset split:")
print("Training :", len(X_train))
print("Testing  :", len(X_test))


# ============================================================
# 4. DEFINE MODELS
# ============================================================

models = {

    "Decision Tree": DecisionTreeClassifier(
        random_state=42,
        max_depth=8
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "SVM RBF": Pipeline([
        (
            "scaler",
            StandardScaler()
        ),

        (
            "classifier",
            SVC(
                kernel="rbf",
                C=10,
                gamma="scale"
            )
        )
    ])
}


# ============================================================
# 5. TRAIN AND EVALUATE
# ============================================================

results = []


for name, model in models.items():

    print("\n" + "=" * 75)
    print("MODEL:", name)
    print("=" * 75)

    print("\nTraining...")

    model.fit(
        X_train,
        y_train
    )

    print("Training complete.")

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    y_pred = model.predict(
        X_test
    )


    # --------------------------------------------------------
    # Accuracy
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    print("\nAccuracy:")
    print(
        f"{accuracy * 100:.2f}%"
    )


    # --------------------------------------------------------
    # Classification report
    # --------------------------------------------------------

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred,
            digits=4
        )
    )


    # --------------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------------

    cm = confusion_matrix(
        y_test,
        y_pred
    )

    print("Confusion Matrix:")
    print(cm)


    # --------------------------------------------------------
    # Store result
    # --------------------------------------------------------

    results.append({
        "Model": name,
        "Accuracy": accuracy
    })


    # --------------------------------------------------------
    # Plot confusion matrix
    # --------------------------------------------------------

    plt.figure(
        figsize=(7, 6)
    )

    plt.imshow(
        cm,
        interpolation="nearest"
    )

    plt.title(
        f"{name} - Fault Signature Confusion Matrix"
    )

    plt.xlabel(
        "Predicted Fault"
    )

    plt.ylabel(
        "Actual Fault"
    )

    plt.colorbar()

    plt.xticks(
        np.arange(6),
        [1, 2, 3, 4, 5, 6]
    )

    plt.yticks(
        np.arange(6),
        [1, 2, 3, 4, 5, 6]
    )


    # Add values to cells

    for i in range(6):

        for j in range(6):

            plt.text(
                j,
                i,
                cm[i, j],
                ha="center",
                va="center"
            )


    plt.tight_layout()


    filename = (
        "outputs/signature_models/"
        + name.lower()
        .replace(" ", "_")
        + "_confusion_matrix.png"
    )

    plt.savefig(
        filename,
        dpi=200
    )

    plt.close()


# ============================================================
# 6. MODEL COMPARISON
# ============================================================

results_df = pd.DataFrame(
    results
)


print("\n" + "=" * 75)
print("BEHAVIORAL SIGNATURE MODEL COMPARISON")
print("=" * 75)

print(
    results_df.to_string(
        index=False
    )
)


# ============================================================
# 7. SAVE RESULTS
# ============================================================

results_df.to_csv(
    "outputs/signature_models/model_comparison.csv",
    index=False
)


# ============================================================
# 8. BEST MODEL
# ============================================================

best_index = (
    results_df["Accuracy"]
    .idxmax()
)

best_model = (
    results_df.loc[
        best_index,
        "Model"
    ]
)

best_accuracy = (
    results_df.loc[
        best_index,
        "Accuracy"
    ]
)


print("\nBest model:")
print(best_model)

print(
    f"Best accuracy: "
    f"{best_accuracy * 100:.2f}%"
)


# ============================================================
# 9. FINAL
# ============================================================

print("\n" + "=" * 75)
print("BEHAVIORAL SIGNATURE ML COMPLETE")
print("=" * 75)

print("\nGenerated files:")

print(
    " - outputs/signature_models/model_comparison.csv"
)

print(
    " - outputs/signature_models/decision_tree_confusion_matrix.png"
)

print(
    " - outputs/signature_models/random_forest_confusion_matrix.png"
)

print(
    " - outputs/signature_models/svm_rbf_confusion_matrix.png"
)

print("=" * 75)