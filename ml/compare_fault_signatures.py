import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances


# ============================================================
# FAULT SIGNATURE COMPARISON
# ============================================================

print("=" * 75)
print("BEHAVIORAL FAULT SIGNATURE COMPARISON")
print("=" * 75)


# ============================================================
# LOAD SIGNATURE DATASET
# ============================================================

df = pd.read_csv(
    "dataset/fault_signatures.csv"
)


# ============================================================
# DEFINE ML FEATURES
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


X = df[FEATURE_COLUMNS].copy()
y = df["fault_id"].copy()


print("\nDataset:")
print("Samples :", len(df))
print("Features:", len(FEATURE_COLUMNS))
print("Faults  :", sorted(y.unique()))


# ============================================================
# MEAN SIGNATURE FOR EACH FAULT
# ============================================================

print("\n" + "=" * 75)
print("MEAN BEHAVIORAL SIGNATURE BY FAULT")
print("=" * 75)


fault_means = (
    df.groupby("fault_id")[FEATURE_COLUMNS]
    .mean()
)


# ============================================================
# IMPORTANT FEATURES
# ============================================================

important_features = [
    "s3_error_count",
    "avg_bit_errors",
    "total_bit_errors",
    "AND_bit_errors",
    "AND_max_bit_errors",
    "AND_avg_bit_errors",
    "max_bit_errors",
    "s2_error_count",
    "OR_bit_errors",
    "OR_avg_bit_errors",
    "OR_result_errors",
    "total_result_errors",
    "AND_result_errors",
    "OR_error_rate",
    "OR_max_bit_errors",
    "AND_error_rate",
    "s0_error_count",
    "XOR_max_bit_errors",
    "error_vectors",
    "XOR_error_rate"
]


print("\nSelected behavioral features:\n")

for feature in important_features:

    if feature in fault_means.columns:

        print("\n" + feature)

        for fault in sorted(fault_means.index):

            print(
                f"  Fault #{fault}: "
                f"{fault_means.loc[fault, feature]:.4f}"
            )


# ============================================================
# STANDARDIZED FAULT CENTROIDS
# ============================================================

scaler = StandardScaler()

scaled_means = scaler.fit_transform(
    fault_means
)


scaled_means_df = pd.DataFrame(
    scaled_means,
    index=fault_means.index,
    columns=fault_means.columns
)


# ============================================================
# DISTANCE BETWEEN FAULT SIGNATURES
# ============================================================

distance_matrix = pairwise_distances(
    scaled_means_df,
    metric="euclidean"
)


distance_df = pd.DataFrame(
    distance_matrix,
    index=[
        f"Fault #{x}"
        for x in fault_means.index
    ],
    columns=[
        f"Fault #{x}"
        for x in fault_means.index
    ]
)


print("\n" + "=" * 75)
print("STANDARDIZED FAULT SIGNATURE DISTANCE")
print("=" * 75)

print(
    distance_df.round(2).to_string()
)


# ============================================================
# CLOSEST FAULT PAIRS
# ============================================================

pairs = []

fault_ids = sorted(
    fault_means.index
)


for i in range(len(fault_ids)):

    for j in range(i + 1, len(fault_ids)):

        f1 = fault_ids[i]
        f2 = fault_ids[j]

        distance = distance_df.loc[
            f"Fault #{f1}",
            f"Fault #{f2}"
        ]

        pairs.append(
            (f1, f2, distance)
        )


pairs.sort(
    key=lambda x: x[2]
)


print("\n" + "=" * 75)
print("CLOSEST FAULT PAIRS")
print("=" * 75)


for f1, f2, distance in pairs:

    print(
        f"Fault #{f1} <-> Fault #{f2} : "
        f"{distance:.4f}"
    )


# ============================================================
# WINDOW-LEVEL ANALYSIS
# ============================================================

print("\n" + "=" * 75)
print("WINDOW-LEVEL FAULT OVERLAP")
print("=" * 75)


# Compare every window between faults.

for f1, f2, _ in pairs:

    fault1 = df[
        df["fault_id"] == f1
    ].set_index("window_id")

    fault2 = df[
        df["fault_id"] == f2
    ].set_index("window_id")


    common_windows = sorted(
        set(fault1.index)
        &
        set(fault2.index)
    )


    distances = []


    for window in common_windows:

        a = fault1.loc[
            window,
            FEATURE_COLUMNS
        ].values.reshape(1, -1)

        b = fault2.loc[
            window,
            FEATURE_COLUMNS
        ].values.reshape(1, -1)


        a = scaler.transform(a)

        b = scaler.transform(b)


        d = np.linalg.norm(
            a - b
        )


        distances.append(d)


    if distances:

        print(
            f"\nFault #{f1} vs Fault #{f2}"
        )

        print(
            f"  Mean distance : "
            f"{np.mean(distances):.4f}"
        )

        print(
            f"  Min distance  : "
            f"{np.min(distances):.4f}"
        )

        print(
            f"  Max distance  : "
            f"{np.max(distances):.4f}"
        )


# ============================================================
# SAVE OUTPUT
# ============================================================

output_path = (
    "outputs/signature_models/"
    "fault_signature_distance.csv"
)


distance_df.to_csv(
    output_path
)


print("\n" + "=" * 75)
print("SIGNATURE COMPARISON COMPLETE")
print("=" * 75)

print(
    f"\nGenerated:\n"
    f" - {output_path}"
)
