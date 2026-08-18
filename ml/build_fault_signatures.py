import pandas as pd
import numpy as np
import os

# ============================================================
# AI-ASSISTED RTL VERIFICATION & BUG DIAGNOSIS
#
# BUILD BEHAVIORAL FAULT SIGNATURES
# ============================================================

INPUT_FILE = "dataset/fault_dataset.csv"
OUTPUT_FILE = "dataset/fault_signatures.csv"

WINDOW_SIZE = 32


# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 75)
print("BUILDING BEHAVIORAL FAULT SIGNATURES")
print("=" * 75)

print("\nRaw dataset:")
print("Rows   :", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 2. ENSURE NUMERIC DATA
# ============================================================

numeric_columns = [
    "fault_id",
    "A",
    "B",
    "OP",
    "expected_result",
    "expected_carry",
    "actual_result",
    "actual_carry",
    "result_error",
    "carry_error",
    "bit_errors"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="raise"
    ).astype(int)


# ============================================================
# 3. RECONSTRUCT VECTOR INDEX FOR EACH FAULT
# ============================================================
#
# The master testbench stores:
#
# Vector 0 -> F1 F2 F3 F4 F5 F6
# Vector 1 -> F1 F2 F3 F4 F5 F6
# Vector 2 -> F1 F2 F3 F4 F5 F6
# ...
#
# Therefore we create a separate vector index inside
# each fault class.
# ============================================================

df["vector_index"] = (
    df.groupby("fault_id")
      .cumcount()
)


# ============================================================
# 4. VERIFY NUMBER OF VECTORS
# ============================================================

vectors_per_fault = (
    df.groupby("fault_id")["vector_index"]
      .count()
)

print("\nVectors per fault:")

print(vectors_per_fault)


if not all(vectors_per_fault == 1024):

    raise ValueError(
        "Each fault must contain exactly 1024 vectors."
    )


# ============================================================
# 5. CREATE WINDOW INDEX
# ============================================================

df["window_id"] = (
    df["vector_index"] // WINDOW_SIZE
)


# ============================================================
# 6. OPERATION NAMES
# ============================================================

operation_names = {
    0: "ADD",
    1: "AND",
    2: "OR",
    3: "XOR"
}


# ============================================================
# 7. HELPER FUNCTION
# ============================================================

def add_operation_features(
    output,
    group,
    operation,
    prefix
):
    """
    Generate behavioral statistics for one ALU operation.
    """

    op_data = group[
        group["OP"] == operation
    ]

    total = len(op_data)

    # --------------------------------------------------------
    # If operation exists
    # --------------------------------------------------------

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

        output[
            f"{prefix}_tests"
        ] = total

        output[
            f"{prefix}_result_errors"
        ] = result_errors

        output[
            f"{prefix}_carry_errors"
        ] = carry_errors

        output[
            f"{prefix}_bit_errors"
        ] = bit_errors

        output[
            f"{prefix}_error_rate"
        ] = (
            (result_errors + carry_errors)
            / total
        )

        output[
            f"{prefix}_avg_bit_errors"
        ] = (
            bit_errors / total
        )

        output[
            f"{prefix}_max_bit_errors"
        ] = (
            op_data["bit_errors"].max()
        )

    else:

        output[
            f"{prefix}_tests"
        ] = 0

        output[
            f"{prefix}_result_errors"
        ] = 0

        output[
            f"{prefix}_carry_errors"
        ] = 0

        output[
            f"{prefix}_bit_errors"
        ] = 0

        output[
            f"{prefix}_error_rate"
        ] = 0

        output[
            f"{prefix}_avg_bit_errors"
        ] = 0

        output[
            f"{prefix}_max_bit_errors"
        ] = 0


# ============================================================
# 8. BUILD SIGNATURES
# ============================================================

signatures = []


for fault_id in sorted(
    df["fault_id"].unique()
):

    fault_data = df[
        df["fault_id"] == fault_id
    ].copy()


    # --------------------------------------------------------
    # Process each 32-vector window
    # --------------------------------------------------------

    for window_id in sorted(
        fault_data["window_id"].unique()
    ):

        window = fault_data[
            fault_data["window_id"] == window_id
        ].copy()


        signature = {

            # ----------------------------------------------
            # Target
            # ----------------------------------------------

            "fault_id": fault_id,

            # ----------------------------------------------
            # Window information
            # ----------------------------------------------

            "window_id": window_id,

            # ----------------------------------------------
            # Number of vectors
            # ----------------------------------------------

            "num_vectors": len(window),

            # ----------------------------------------------
            # Overall behavioral statistics
            # ----------------------------------------------

            "total_result_errors":
                window["result_error"].sum(),

            "total_carry_errors":
                window["carry_error"].sum(),

            "total_bit_errors":
                window["bit_errors"].sum(),

            "error_vectors":
                (
                    (
                        window["result_error"] == 1
                    )
                    |
                    (
                        window["carry_error"] == 1
                    )
                ).sum(),

            "error_rate":
                (
                    (
                        (
                            window["result_error"] == 1
                        )
                        |
                        (
                            window["carry_error"] == 1
                        )
                    ).sum()
                    / len(window)
                ),

            "avg_bit_errors":
                window["bit_errors"].mean(),

            "max_bit_errors":
                window["bit_errors"].max(),

            # ----------------------------------------------
            # Input statistics
            # ----------------------------------------------

            "avg_A":
                window["A"].mean(),

            "avg_B":
                window["B"].mean(),

            "avg_OP":
                window["OP"].mean(),

            "A_ones_total":
                window["A"].apply(
                    lambda x: bin(int(x)).count("1")
                ).sum(),

            "B_ones_total":
                window["B"].apply(
                    lambda x: bin(int(x)).count("1")
                ).sum()
        }


        # ====================================================
        # 9. OPERATION-SPECIFIC FEATURES
        # ====================================================

        add_operation_features(
            signature,
            window,
            0,
            "ADD"
        )

        add_operation_features(
            signature,
            window,
            1,
            "AND"
        )

        add_operation_features(
            signature,
            window,
            2,
            "OR"
        )

        add_operation_features(
            signature,
            window,
            3,
            "XOR"
        )


        # ====================================================
        # 10. RESULT BIT ERROR FEATURES
        # ====================================================

        for bit in range(4):

            expected_bit = (
                (window["expected_result"]
                 // (2 ** bit)) % 2
            )

            actual_bit = (
                (window["actual_result"]
                 // (2 ** bit)) % 2
            )

            bit_error = (
                expected_bit != actual_bit
            )

            signature[
                f"s{bit}_error_count"
            ] = bit_error.sum()


        # ====================================================
        # 11. CARRY BEHAVIOR
        # ====================================================

        signature[
            "expected_carry_count"
        ] = window[
            "expected_carry"
        ].sum()

        signature[
            "actual_carry_count"
        ] = window[
            "actual_carry"
        ].sum()


        # ====================================================
        # 12. STORE SIGNATURE
        # ====================================================

        signatures.append(
            signature
        )


# ============================================================
# 13. CREATE SIGNATURE DATAFRAME
# ============================================================

signature_df = pd.DataFrame(
    signatures
)


# ============================================================
# 14. SORT DATA
# ============================================================

signature_df = signature_df.sort_values(
    [
        "fault_id",
        "window_id"
    ]
).reset_index(
    drop=True
)


# ============================================================
# 15. SAVE DATASET
# ============================================================

signature_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 16. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 75)
print("FAULT SIGNATURE DATASET")
print("=" * 75)

print(
    "\nNumber of ML samples:",
    len(signature_df)
)

print(
    "Number of columns:",
    len(signature_df.columns)
)

print(
    "Window size:",
    WINDOW_SIZE
)


# ============================================================
# 17. DISTRIBUTION
# ============================================================

print("\nFault distribution:")

print(
    signature_df[
        "fault_id"
    ].value_counts().sort_index()
)


# ============================================================
# 18. SAMPLE
# ============================================================

print("\nFirst 10 signatures:")

print(
    signature_df.head(10)
    .to_string(index=False)
)


# ============================================================
# 19. SAVE FEATURE INFORMATION
# ============================================================

feature_columns = [
    column
    for column in signature_df.columns
    if column not in [
        "fault_id",
        "window_id"
    ]
]

print("\nML feature count:")
print(len(feature_columns))

print("\nML features:")

for feature in feature_columns:
    print(" -", feature)


# ============================================================
# 20. FINAL
# ============================================================

print("\n" + "=" * 75)
print("FAULT SIGNATURE GENERATION COMPLETE")
print("=" * 75)

print("\nGenerated:")
print(OUTPUT_FILE)

print("\nExpected samples:")
print("6 faults × 32 windows = 192")

print("\nActual samples:")
print(len(signature_df))

print("=" * 75)