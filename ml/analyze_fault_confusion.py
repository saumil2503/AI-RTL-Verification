import pandas as pd
import numpy as np


# ============================================================
# FAULT CONFUSION FEATURE ANALYSIS
# ============================================================

print("=" * 75)
print("FAULT CONFUSION FEATURE ANALYSIS")
print("=" * 75)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    "dataset/fault_signatures.csv"
)


NON_FEATURE_COLUMNS = [
    "fault_id",
    "window_id",
    "num_vectors"
]


FEATURE_COLUMNS = [
    c for c in df.columns
    if c not in NON_FEATURE_COLUMNS
]


print("\nDataset:")
print("Samples :", len(df))
print("Features:", len(FEATURE_COLUMNS))


# ============================================================
# FUNCTION
# ============================================================

def compare_faults(
    fault_a,
    fault_b
):

    print("\n")
    print("=" * 75)
    print(
        f"FAULT {fault_a} vs FAULT {fault_b}"
    )
    print("=" * 75)


    A = df[
        df["fault_id"] == fault_a
    ][FEATURE_COLUMNS]


    B = df[
        df["fault_id"] == fault_b
    ][FEATURE_COLUMNS]


    mean_a = A.mean()
    mean_b = B.mean()


    std_a = A.std()
    std_b = B.std()


    # --------------------------------------------------------
    # Absolute difference
    # --------------------------------------------------------

    difference = (
        mean_a - mean_b
    ).abs()


    # --------------------------------------------------------
    # Pooled standard deviation
    # --------------------------------------------------------

    pooled_std = np.sqrt(
        (
            std_a ** 2
            +
            std_b ** 2
        )
        /
        2
    )


    # Avoid divide by zero

    pooled_std = pooled_std.replace(
        0,
        np.nan
    )


    effect_size = (
        difference
        /
        pooled_std
    )


    result = pd.DataFrame({

        "fault_a_mean":
            mean_a,

        "fault_b_mean":
            mean_b,

        "absolute_difference":
            difference,

        "effect_size":
            effect_size

    })


    result = result.sort_values(
        "effect_size",
        ascending=False
    )


    print(
        "\nTop features separating "
        f"Fault {fault_a} and Fault {fault_b}:"
    )


    print(
        result.head(15).to_string()
    )


    # --------------------------------------------------------
    # Most similar features
    # --------------------------------------------------------

    similar = result.sort_values(
        "effect_size",
        ascending=True
    )


    print(
        "\nMost similar features:"
    )


    print(
        similar.head(15).to_string()
    )


    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    filename = (
        "outputs/signature_models/"
        f"fault_{fault_a}_vs_{fault_b}_features.csv"
    )


    result.to_csv(
        filename
    )


    print(
        f"\nSaved:"
        f"\n - {filename}"
    )


# ============================================================
# IMPORTANT CONFUSIONS
# ============================================================

compare_faults(2, 6)

compare_faults(4, 1)

compare_faults(4, 5)


# ============================================================
# COMPLETE
# ============================================================

print("\n")
print("=" * 75)
print("FEATURE ANALYSIS COMPLETE")
print("=" * 75)