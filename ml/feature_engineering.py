import pandas as pd

# ============================================================
# AI-ASSISTED RTL VERIFICATION & BUG DIAGNOSIS
# FEATURE ENGINEERING
# ============================================================

INPUT_FILE = "dataset/fault_dataset.csv"
OUTPUT_FILE = "dataset/ml_features.csv"


# ============================================================
# 1. LOAD RAW RTL DATASET
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("FEATURE ENGINEERING")
print("=" * 70)

print("\nRaw dataset:")
print("Rows   :", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 2. CONVERT NUMERIC COLUMNS TO INTEGER
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
    df[column] = pd.to_numeric(df[column], errors="raise").astype(int)


# ============================================================
# 3. CREATE OPERATION LABEL
# ============================================================

operation_names = {
    0: "ADD",
    1: "AND",
    2: "OR",
    3: "XOR"
}

df["operation"] = df["OP"].map(operation_names)


# ============================================================
# 4. EXTRACT EXPECTED AND ACTUAL RESULT BITS
# ============================================================
#
# Instead of using:
#
#     value >> bit
#
# we use:
#
#     (value // 2**bit) % 2
#
# This works reliably with Pandas Series.
# ============================================================

for bit in range(4):

    df[f"expected_s{bit}"] = (
        (df["expected_result"] // (2 ** bit)) % 2
    ).astype(int)

    df[f"actual_s{bit}"] = (
        (df["actual_result"] // (2 ** bit)) % 2
    ).astype(int)


# ============================================================
# 5. CREATE INDIVIDUAL OUTPUT-BIT ERROR FEATURES
# ============================================================

for bit in range(4):

    df[f"s{bit}_error"] = (
        df[f"expected_s{bit}"]
        != df[f"actual_s{bit}"]
    ).astype(int)


# ============================================================
# 6. CREATE INPUT BIT FEATURES
# ============================================================

for bit in range(4):

    df[f"A{bit}"] = (
        (df["A"] // (2 ** bit)) % 2
    ).astype(int)

    df[f"B{bit}"] = (
        (df["B"] // (2 ** bit)) % 2
    ).astype(int)


# ============================================================
# 7. CREATE INPUT BIT COUNT FEATURES
# ============================================================

df["A_ones"] = df["A"].apply(
    lambda x: bin(int(x)).count("1")
)

df["B_ones"] = df["B"].apply(
    lambda x: bin(int(x)).count("1")
)


# ============================================================
# 8. CALCULATE TOTAL OUTPUT BIT ERRORS
# ============================================================

df["calculated_bit_errors"] = (
    df["s0_error"]
    + df["s1_error"]
    + df["s2_error"]
    + df["s3_error"]
)


# ============================================================
# 9. VERIFY BIT ERROR CALCULATION
# ============================================================

difference_count = (
    df["calculated_bit_errors"]
    != df["bit_errors"]
).sum()

print("\nBit-error verification:")

if difference_count == 0:
    print("PASS: Calculated bit errors match RTL dataset.")
else:
    print(
        "WARNING:",
        difference_count,
        "rows do not match."
    )


# ============================================================
# 10. CREATE OVERALL OUTPUT ERROR
# ============================================================

df["output_error"] = (
    (df["result_error"] == 1)
    |
    (df["carry_error"] == 1)
).astype(int)


# ============================================================
# 11. CREATE CARRY MISMATCH
# ============================================================

df["carry_mismatch"] = (
    df["expected_carry"]
    != df["actual_carry"]
).astype(int)


# ============================================================
# 12. SELECT ML FEATURES
# ============================================================
#
# IMPORTANT:
#
# fault_id is NOT an input feature.
#
# fault_id is the target that the ML model must predict.
# ============================================================

feature_columns = [

    # Input operands
    "A",
    "B",

    # Operation
    "OP",

    # Expected circuit behaviour
    "expected_result",
    "expected_carry",

    # Observed circuit behaviour
    "actual_result",
    "actual_carry",

    # Error information
    "result_error",
    "carry_error",
    "bit_errors",

    # Individual output-bit errors
    "s0_error",
    "s1_error",
    "s2_error",
    "s3_error",

    # Individual A input bits
    "A0",
    "A1",
    "A2",
    "A3",

    # Individual B input bits
    "B0",
    "B1",
    "B2",
    "B3",

    # Input statistics
    "A_ones",
    "B_ones",

    # Overall error
    "output_error",

    # Carry mismatch
    "carry_mismatch"
]


# ============================================================
# 13. CREATE FINAL ML DATASET
# ============================================================

ml_df = df[
    feature_columns + ["fault_id"]
].copy()


# ============================================================
# 14. SAVE DATASET
# ============================================================

ml_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 15. DISPLAY RESULTS
# ============================================================

print("\nML feature dataset:")
print("Rows   :", len(ml_df))
print("Columns:", len(ml_df.columns))

print("\nML features:")

for column in feature_columns:
    print(" -", column)

print("\nTarget:")
print(" - fault_id")


# ============================================================
# 16. TARGET DISTRIBUTION
# ============================================================

print("\nTarget distribution:")

print(
    ml_df["fault_id"]
    .value_counts()
    .sort_index()
)


# ============================================================
# 17. DISPLAY SAMPLE DATA
# ============================================================

print("\nFirst 10 ML samples:")

print(
    ml_df.head(10)
    .to_string(index=False)
)


# ============================================================
# 18. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 70)

print("\nGenerated file:")
print(OUTPUT_FILE)

print("\nTarget column:")
print("fault_id")

print("\nTotal ML samples:")
print(len(ml_df))

print("=" * 70)