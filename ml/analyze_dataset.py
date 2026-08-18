import pandas as pd

# ============================================================
# AI-Assisted RTL Verification
# Dataset Analysis
# ============================================================

# Load dataset
df = pd.read_csv("dataset/fault_dataset.csv")
print("=" * 70)
print("AI-ASSISTED RTL VERIFICATION DATASET ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# Basic information
# ------------------------------------------------------------

print("\nDataset shape:")
print(df.shape)

print("\nNumber of rows:", len(df))
print("Number of columns:", len(df.columns))

# ------------------------------------------------------------
# Column names
# ------------------------------------------------------------

print("\nColumns:")
for column in df.columns:
    print(" -", column)

# ------------------------------------------------------------
# Missing values
# ------------------------------------------------------------

print("\nMissing values:")
print(df.isnull().sum())

# ------------------------------------------------------------
# Fault distribution
# ------------------------------------------------------------

print("\nFault distribution:")
print(df["fault_id"].value_counts().sort_index())

# ------------------------------------------------------------
# Error distribution
# ------------------------------------------------------------

print("\nError distribution:")
print(df["result_error"].value_counts())

print("\nCarry error distribution:")
print(df["carry_error"].value_counts())

# ------------------------------------------------------------
# Bit error distribution
# ------------------------------------------------------------

print("\nBit error distribution:")
print(df["bit_errors"].value_counts().sort_index())

# ------------------------------------------------------------
# Failures by fault
# ------------------------------------------------------------

print("\nFailures by fault:")

failure_summary = (
    df.groupby("fault_id")["result_error"]
    .sum()
)

print(failure_summary)

# ------------------------------------------------------------
# Total failures
# ------------------------------------------------------------

print("\nTotal faulty observations:")

total_failures = (
    (df["result_error"] == 1) |
    (df["carry_error"] == 1)
).sum()

print(total_failures)

# ------------------------------------------------------------
# Fault-wise failure percentage
# ------------------------------------------------------------

print("\nFault-wise failure percentage:")

for fault in sorted(df["fault_id"].unique()):

    fault_data = df[df["fault_id"] == fault]

    failures = (
        (fault_data["result_error"] == 1) |
        (fault_data["carry_error"] == 1)
    ).sum()

    percentage = failures / len(fault_data) * 100

    print(
        f"Fault #{fault}: "
        f"{failures}/{len(fault_data)} "
        f"({percentage:.2f}%)"
    )

# ------------------------------------------------------------
# Operations
# ------------------------------------------------------------

print("\nOperation distribution:")

print(
    df["OP"]
    .value_counts()
    .sort_index()
)

# ------------------------------------------------------------
# First rows
# ------------------------------------------------------------

print("\nFirst 10 rows:")
print(df.head(10).to_string(index=False))

# ------------------------------------------------------------
# Last rows
# ------------------------------------------------------------

print("\nLast 10 rows:")
print(df.tail(10).to_string(index=False))

print("\n" + "=" * 70)
print("DATASET ANALYSIS COMPLETE")
print("=" * 70)