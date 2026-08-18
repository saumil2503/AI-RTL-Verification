# ============================================================
# AI-ASSISTED RTL FAULT DIAGNOSIS
# RAW VERIFICATION DATA -> AI DIAGNOSIS
#
# Project 2:
# AI-Assisted RTL Verification & Bug Diagnosis
# ============================================================

import pandas as pd
import numpy as np
import joblib
import os


# ============================================================
# PATHS
# ============================================================

DATASET_FILE = "dataset/fault_dataset.csv"

# FINAL TRAINED MODEL
MODEL_FILE = "outputs/final_model/final_random_forest.pkl"

# FINAL 46-FEATURE LIST
FEATURE_FILE = "outputs/final_model/final_feature_list.csv"

WINDOW_SIZE = 32


# ============================================================
# FAULT INFORMATION
# ============================================================

FAULT_INFO = {

    1: {
        "name": "ADD Carry Fault",
        "operation": "ADD",
        "description":
            "ADD operation does not generate the correct carry output."
    },

    2: {
        "name": "AND-to-OR Logic Fault",
        "operation": "AND",
        "description":
            "AND operation is incorrectly implemented as OR."
    },

    3: {
        "name": "XOR-to-XNOR Logic Fault",
        "operation": "XOR",
        "description":
            "XOR operation is incorrectly implemented as XNOR."
    },

    4: {
        "name": "OR-to-XOR Logic Fault",
        "operation": "OR",
        "description":
            "OR operation is incorrectly implemented as XOR."
    },

    5: {
        "name": "Opcode Selection Fault",
        "operation": "OR",
        "description":
            "The opcode incorrectly selects the AND operation instead of OR."
    },

    6: {
        "name": "Inverted B Operand Fault",
        "operation": "AND",
        "description":
            "The AND operation uses an inverted B input."
    }
}


# ============================================================
# HEADER
# ============================================================

print("=" * 75)
print("        AI RTL FAULT DIAGNOSIS ENGINE")
print("=" * 75)


# ============================================================
# CHECK REQUIRED FILES
# ============================================================

print("\nChecking project files...")

required_files = [
    DATASET_FILE,
    MODEL_FILE,
    FEATURE_FILE
]

for file_path in required_files:

    if not os.path.exists(file_path):

        print("\nERROR: Required file not found:")
        print(" ", file_path)

        print("\nMake sure you are running this command")
        print("from the project root directory:")

        print("\n  python ml\\real_time_diagnosis.py")

        raise FileNotFoundError(file_path)

    else:

        print("FOUND:", file_path)


# ============================================================
# LOAD FINAL MODEL
# ============================================================

print("\n" + "=" * 75)
print("LOADING FINAL AI MODEL")
print("=" * 75)

print("\nLoading trained Random Forest model...")

model = joblib.load(MODEL_FILE)

print("Model loaded successfully.")


# ============================================================
# LOAD FEATURE LIST
# ============================================================

feature_df = pd.read_csv(FEATURE_FILE)

feature_list = feature_df["feature"].tolist()

print("\nExpected ML features:", len(feature_list))

if len(feature_list) != 46:

    raise ValueError(
        f"Expected 46 ML features, but found {len(feature_list)}."
    )


# ============================================================
# LOAD RAW DATASET
# ============================================================

df = pd.read_csv(DATASET_FILE)

print("\nRaw verification dataset:")
print("Rows   :", len(df))
print("Columns:", len(df.columns))


# ============================================================
# CREATE VECTOR INDEX
# ============================================================

df["vector_index"] = (
    df.groupby("fault_id").cumcount()
)

df["window_id"] = (
    df["vector_index"] // WINDOW_SIZE
)


# ============================================================
# OPERATION NAMES
# ============================================================

operation_names = {
    0: "ADD",
    1: "AND",
    2: "OR",
    3: "XOR"
}


# ============================================================
# FEATURE GENERATION FUNCTION
# ============================================================

def create_signature(window):

    signature = {}

    # --------------------------------------------------------
    # Basic behavioral statistics
    # --------------------------------------------------------

    signature["num_vectors"] = len(window)

    signature["total_result_errors"] = (
        window["result_error"].sum()
    )

    signature["total_carry_errors"] = (
        window["carry_error"].sum()
    )

    signature["total_bit_errors"] = (
        window["bit_errors"].sum()
    )

    signature["error_vectors"] = (
        (
            (window["result_error"] == 1)
            |
            (window["carry_error"] == 1)
        ).sum()
    )

    signature["error_rate"] = (
        signature["error_vectors"]
        / len(window)
    )

    signature["avg_bit_errors"] = (
        window["bit_errors"].mean()
    )

    signature["max_bit_errors"] = (
        window["bit_errors"].max()
    )

    # --------------------------------------------------------
    # Input statistics
    # --------------------------------------------------------

    signature["avg_A"] = window["A"].mean()

    signature["avg_B"] = window["B"].mean()

    signature["avg_OP"] = window["OP"].mean()

    signature["A_ones_total"] = (
        window["A"]
        .apply(lambda x: bin(int(x)).count("1"))
        .sum()
    )

    signature["B_ones_total"] = (
        window["B"]
        .apply(lambda x: bin(int(x)).count("1"))
        .sum()
    )

    # --------------------------------------------------------
    # Operation-specific features
    # --------------------------------------------------------

    for operation, prefix in [
        (0, "ADD"),
        (1, "AND"),
        (2, "OR"),
        (3, "XOR")
    ]:

        op_data = window[
            window["OP"] == operation
        ]

        total = len(op_data)

        signature[f"{prefix}_tests"] = total

        if total > 0:

            result_errors = (
                op_data["result_error"].sum()
            )

            carry_errors = (
                op_data["carry_error"].sum()
            )

            bit_errors = (
                op_data["bit_errors"].sum()
            )

            signature[
                f"{prefix}_result_errors"
            ] = result_errors

            signature[
                f"{prefix}_carry_errors"
            ] = carry_errors

            signature[
                f"{prefix}_bit_errors"
            ] = bit_errors

            signature[
                f"{prefix}_error_rate"
            ] = (
                (result_errors + carry_errors)
                / total
            )

            signature[
                f"{prefix}_avg_bit_errors"
            ] = (
                bit_errors / total
            )

            signature[
                f"{prefix}_max_bit_errors"
            ] = (
                op_data["bit_errors"].max()
            )

        else:

            signature[
                f"{prefix}_result_errors"
            ] = 0

            signature[
                f"{prefix}_carry_errors"
            ] = 0

            signature[
                f"{prefix}_bit_errors"
            ] = 0

            signature[
                f"{prefix}_error_rate"
            ] = 0

            signature[
                f"{prefix}_avg_bit_errors"
            ] = 0

            signature[
                f"{prefix}_max_bit_errors"
            ] = 0

    # --------------------------------------------------------
    # Individual result bit errors
    # --------------------------------------------------------

    for bit in range(4):

        expected_bit = (
            (
                window["expected_result"]
                // (2 ** bit)
            ) % 2
        )

        actual_bit = (
            (
                window["actual_result"]
                // (2 ** bit)
            ) % 2
        )

        bit_error = (
            expected_bit != actual_bit
        )

        signature[
            f"s{bit}_error_count"
        ] = bit_error.sum()

    # --------------------------------------------------------
    # Carry behavior
    # --------------------------------------------------------

    signature["expected_carry_count"] = (
        window["expected_carry"].sum()
    )

    signature["actual_carry_count"] = (
        window["actual_carry"].sum()
    )

    return signature


# ============================================================
# AVAILABLE FAULTS
# ============================================================

faults = sorted(
    df["fault_id"].unique()
)

print("\n" + "=" * 75)
print("AVAILABLE FAULT DATASETS")
print("=" * 75)

for fault_id in faults:

    print(
        f"Fault #{fault_id} : "
        f"{FAULT_INFO.get(fault_id, {}).get('name', 'Unknown')}"
    )


# ============================================================
# USER SELECTION
# ============================================================

print("\nSelect a fault dataset for demonstration.")

try:

    fault_id = int(
        input("Fault ID (1-6): ")
    )

except ValueError:

    raise ValueError(
        "Fault ID must be an integer from 1 to 6."
    )


if fault_id not in faults:

    raise ValueError(
        "Invalid fault ID. Enter a value from 1 to 6."
    )


# ============================================================
# AVAILABLE WINDOWS
# ============================================================

fault_data = df[
    df["fault_id"] == fault_id
].copy()

windows = sorted(
    fault_data["window_id"].unique()
)

print(
    f"\nAvailable behavioral windows "
    f"for Fault #{fault_id}:"
)

print(windows)

try:

    window_id = int(
        input("Window ID (0-31): ")
    )

except ValueError:

    raise ValueError(
        "Window ID must be an integer from 0 to 31."
    )


if window_id not in windows:

    raise ValueError(
        "Invalid window ID."
    )


# ============================================================
# SELECT WINDOW
# ============================================================

window = fault_data[
    fault_data["window_id"] == window_id
].copy()

print("\n" + "=" * 75)
print("BEHAVIORAL WINDOW")
print("=" * 75)

print("Fault dataset :", fault_id)
print("Window ID     :", window_id)
print("Vectors       :", len(window))


# ============================================================
# BUILD SIGNATURE
# ============================================================

signature = create_signature(window)

signature_df = pd.DataFrame(
    [signature]
)


# ============================================================
# VERIFY FEATURE AVAILABILITY
# ============================================================

missing_features = [
    feature
    for feature in feature_list
    if feature not in signature_df.columns
]

if missing_features:

    print("\nERROR: Missing ML features:")

    for feature in missing_features:
        print(" -", feature)

    raise ValueError(
        "Feature mismatch between signature generator "
        "and final trained model."
    )


# ============================================================
# SELECT EXACT 46 MODEL FEATURES
# ============================================================

X = signature_df[
    feature_list
].copy()


print("\nML feature vector:")
print("Samples :", len(X))
print("Features:", len(X.columns))


# ============================================================
# AI PREDICTION
# ============================================================

prediction = model.predict(X)[0]

probabilities = model.predict_proba(X)[0]

classes = model.classes_


# ============================================================
# PREDICTION CONFIDENCE
# ============================================================

confidence = (
    probabilities[
        list(classes).index(prediction)
    ] * 100
)


# ============================================================
# DISPLAY DIAGNOSIS
# ============================================================

info = FAULT_INFO[int(prediction)]

print("\n" + "=" * 75)
print("                    AI DIAGNOSIS")
print("=" * 75)

print(
    f"\nPredicted Fault   : FAULT #{prediction}"
)

print(
    f"Fault Name        : {info['name']}"
)

print(
    f"Affected Operation: {info['operation']}"
)

print(
    f"Confidence        : {confidence:.2f}%"
)

print("\nFault Description:")

print(
    f"  {info['description']}"
)


# ============================================================
# PROBABILITY DISTRIBUTION
# ============================================================

print("\n" + "=" * 75)
print("              FAULT PROBABILITY DISTRIBUTION")
print("=" * 75)

probability_pairs = sorted(
    zip(classes, probabilities),
    key=lambda x: x[1],
    reverse=True
)

for fault, probability in probability_pairs:

    print(
        f"Fault #{fault} : "
        f"{probability * 100:6.2f}%"
    )


# ============================================================
# BEHAVIORAL SUMMARY
# ============================================================

print("\n" + "=" * 75)
print("              BEHAVIORAL SIGNATURE")
print("=" * 75)

print(
    f"\nTotal result errors : "
    f"{signature['total_result_errors']}"
)

print(
    f"Total carry errors  : "
    f"{signature['total_carry_errors']}"
)

print(
    f"Total bit errors    : "
    f"{signature['total_bit_errors']}"
)

print(
    f"Error vectors       : "
    f"{signature['error_vectors']}"
)

print(
    f"Error rate          : "
    f"{signature['error_rate']:.4f}"
)

print(
    f"Average bit errors  : "
    f"{signature['avg_bit_errors']:.4f}"
)

print(
    f"Maximum bit errors  : "
    f"{signature['max_bit_errors']}"
)


# ============================================================
# OPERATION ERROR SUMMARY
# ============================================================

print("\n" + "=" * 75)
print("              OPERATION ERROR SUMMARY")
print("=" * 75)

for prefix in [
    "ADD",
    "AND",
    "OR",
    "XOR"
]:

    print(
        f"\n{prefix}:"
    )

    print(
        f"  Tests         : "
        f"{signature[prefix + '_tests']}"
    )

    print(
        f"  Result errors : "
        f"{signature[prefix + '_result_errors']}"
    )

    print(
        f"  Carry errors  : "
        f"{signature[prefix + '_carry_errors']}"
    )

    print(
        f"  Bit errors    : "
        f"{signature[prefix + '_bit_errors']}"
    )

    print(
        f"  Error rate    : "
        f"{signature[prefix + '_error_rate']:.4f}"
    )


# ============================================================
# BIT ERROR SUMMARY
# ============================================================

print("\n" + "=" * 75)
print("              RESULT BIT ERROR SUMMARY")
print("=" * 75)

for bit in range(4):

    print(
        f"s{bit} error count : "
        f"{signature[f's{bit}_error_count']}"
    )


# ============================================================
# PREDICTION VERIFICATION
# ============================================================

print("\n" + "=" * 75)
print("              PREDICTION VERIFICATION")
print("=" * 75)

print(
    f"\nActual hidden fault : #{fault_id}"
)

print(
    f"AI predicted fault : #{prediction}"
)

if int(prediction) == int(fault_id):

    print(
        "\nRESULT: CORRECT PREDICTION"
    )

else:

    print(
        "\nRESULT: INCORRECT PREDICTION"
    )


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 75)
print("                FINAL AI RESULT")
print("=" * 75)

print(
    f"\nPredicted Fault : #{prediction}"
)

print(
    f"Fault           : {info['name']}"
)

print(
    f"Operation       : {info['operation']}"
)

print(
    f"Confidence      : {confidence:.2f}%"
)

print(
    "\nThe final Random Forest analyzed the "
    "46-feature behavioral signature generated "
    "from the RTL verification results and "
    "selected the most likely fault class."
)

print("\n" + "=" * 75)
print("             FAULT DIAGNOSIS COMPLETE")
print("=" * 75)