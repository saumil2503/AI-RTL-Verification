# ============================================================
# AI-ASSISTED RTL VERIFICATION & FAULT DIAGNOSIS DASHBOARD
# ============================================================
#
# Project:
#   4-BIT ALU RTL VERIFICATION + MACHINE LEARNING
#
# Final Model:
#   Random Forest - 500 Trees
#
# ML Features:
#   46 Behavioral Features
#
# Fault Classes:
#   6
#
# Validation:
#   End-to-End       : 96.88%
#   Group CV         : 95.31% +/- 2.27%
#
# Run:
#   python -m streamlit run app.py
#
# ============================================================

import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI RTL Fault Diagnosis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent

MODEL_PATH = ROOT / "models" / "final_fault_classifier.pkl"
FEATURE_PATH = ROOT / "models" / "model_features.csv"

RAW_DATASET_PATH = ROOT / "dataset" / "fault_dataset.csv"
SIGNATURE_DATASET_PATH = ROOT / "dataset" / "fault_signatures.csv"

IMPORTANCE_PATH = (
    ROOT /
    "outputs" /
    "signature_models" /
    "feature_importance.csv"
)

PREDICTIONS_PATH = (
    ROOT /
    "outputs" /
    "final_model" /
    "all_predictions.csv"
)

MODEL_COMPARISON_PATH = (
    ROOT /
    "outputs" /
    "signature_models" /
    "model_comparison.csv"
)


# ============================================================
# 3. FAULT INFORMATION
# ============================================================

FAULT_INFO = {

    1: {
        "name": "ADD Carry Fault",
        "operation": "ADD",
        "description":
            "ADD produces the correct 4-bit result "
            "but fails to generate the correct carry output.",
        "rtl":
            "ADD carry generation intentionally broken."
    },

    2: {
        "name": "AND-to-OR Logic Fault",
        "operation": "AND",
        "description":
            "AND operation is intentionally implemented as OR.",
        "rtl":
            "RESULT = A | B instead of A & B."
    },

    3: {
        "name": "XOR-to-XNOR Logic Fault",
        "operation": "XOR",
        "description":
            "XOR operation is intentionally implemented as XNOR.",
        "rtl":
            "RESULT = ~(A ^ B) instead of A ^ B."
    },

    4: {
        "name": "OR-to-XOR Logic Fault",
        "operation": "OR",
        "description":
            "OR operation is intentionally implemented as XOR.",
        "rtl":
            "RESULT = A ^ B instead of A | B."
    },

    5: {
        "name": "Opcode Selection Fault",
        "operation": "OR",
        "description":
            "OP=10 incorrectly selects the AND operation instead of OR.",
        "rtl":
            "OP=10 selects AND instead of OR."
    },

    6: {
        "name": "Inverted B Operand Fault",
        "operation": "AND",
        "description":
            "AND operation uses an inverted B operand.",
        "rtl":
            "AND operation uses ~B instead of B."
    }
}


OPERATIONS = {
    0: "ADD",
    1: "AND",
    2: "OR",
    3: "XOR"
}


# ============================================================
# 4. FALLBACK MODEL FEATURES
# ============================================================

FALLBACK_FEATURES = [

    "total_result_errors",
    "total_carry_errors",
    "total_bit_errors",
    "error_vectors",
    "error_rate",
    "avg_bit_errors",
    "max_bit_errors",

    "avg_A",
    "avg_B",
    "avg_OP",

    "A_ones_total",
    "B_ones_total",

    "ADD_tests",
    "ADD_result_errors",
    "ADD_carry_errors",
    "ADD_bit_errors",
    "ADD_error_rate",
    "ADD_avg_bit_errors",
    "ADD_max_bit_errors",

    "AND_tests",
    "AND_result_errors",
    "AND_carry_errors",
    "AND_bit_errors",
    "AND_error_rate",
    "AND_avg_bit_errors",
    "AND_max_bit_errors",

    "OR_tests",
    "OR_result_errors",
    "OR_carry_errors",
    "OR_bit_errors",
    "OR_error_rate",
    "OR_avg_bit_errors",
    "OR_max_bit_errors",

    "XOR_tests",
    "XOR_result_errors",
    "XOR_carry_errors",
    "XOR_error_rate",
    "XOR_avg_bit_errors",
    "XOR_max_bit_errors",

    "s0_error_count",
    "s1_error_count",
    "s2_error_count",
    "s3_error_count",

    "expected_carry_count",
    "actual_carry_count"
]


# ============================================================
# 5. LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    return joblib.load(
        MODEL_PATH
    )


@st.cache_data
def load_model_features():

    if FEATURE_PATH.exists():

        df = pd.read_csv(
            FEATURE_PATH
        )

        if (
            "feature" in df.columns
            and len(df) == 46
        ):

            return df["feature"].astype(
                str
            ).tolist()

    return FALLBACK_FEATURES.copy()


@st.cache_data
def load_signature_dataset():

    if not SIGNATURE_DATASET_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(
        SIGNATURE_DATASET_PATH
    )


@st.cache_data
def load_feature_importance():

    if not IMPORTANCE_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(
        IMPORTANCE_PATH
    )


@st.cache_data
def load_predictions():

    if not PREDICTIONS_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(
        PREDICTIONS_PATH
    )


# ============================================================
# 6. CHECK MODEL
# ============================================================

if not MODEL_PATH.exists():

    st.error(
        "Final Random Forest model was not found."
    )

    st.code(
        "python ml/final_model.py"
    )

    st.stop()


MODEL = load_model()
MODEL_FEATURES = load_model_features()


# ============================================================
# 7. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }

    .subtitle {
        color: #9aa4b2;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }

    .success-box {
        padding: 1rem;
        border-radius: 12px;
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.35);
    }

    .warning-box {
        padding: 1rem;
        border-radius: 12px;
        background: rgba(245,158,11,0.12);
        border: 1px solid rgba(245,158,11,0.35);
    }

    .danger-box {
        padding: 1rem;
        border-radius: 12px;
        background: rgba(239,68,68,0.12);
        border: 1px solid rgba(239,68,68,0.35);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 8. HELPER FUNCTIONS
# ============================================================

def bit_count(value):

    try:

        return bin(
            int(value) & 0xF
        ).count("1")

    except Exception:

        return 0


# ------------------------------------------------------------
# Operation statistics
# ------------------------------------------------------------

def calculate_operation_stats(
    group,
    operation
):

    data = group[
        group["OP"] == operation
    ]

    total = len(data)

    if total == 0:

        return {
            "tests": 0,
            "result_errors": 0,
            "carry_errors": 0,
            "bit_errors": 0,
            "error_rate": 0.0,
            "avg_bit_errors": 0.0,
            "max_bit_errors": 0
        }

    result_errors = int(
        data["result_error"].sum()
    )

    carry_errors = int(
        data["carry_error"].sum()
    )

    bit_errors = int(
        data["bit_errors"].sum()
    )

    error_vectors = int(
        (
            (data["result_error"] != 0)
            |
            (data["carry_error"] != 0)
        ).sum()
    )

    return {

        "tests": total,

        "result_errors":
            result_errors,

        "carry_errors":
            carry_errors,

        "bit_errors":
            bit_errors,

        "error_rate":
            error_vectors / total,

        "avg_bit_errors":
            float(
                data["bit_errors"].mean()
            ),

        "max_bit_errors":
            int(
                data["bit_errors"].max()
            )
    }


# ------------------------------------------------------------
# Build behavioral signature
# ------------------------------------------------------------

def build_signature(
    group,
    fault_id=None,
    window_id=None
):

    group = group.copy()

    total_vectors = len(group)

    error_mask = (
        (group["result_error"] != 0)
        |
        (group["carry_error"] != 0)
    )

    signature = {

        "total_result_errors":
            int(
                group["result_error"].sum()
            ),

        "total_carry_errors":
            int(
                group["carry_error"].sum()
            ),

        "total_bit_errors":
            int(
                group["bit_errors"].sum()
            ),

        "error_vectors":
            int(
                error_mask.sum()
            ),

        "error_rate":
            float(
                error_mask.mean()
            ),

        "avg_bit_errors":
            float(
                group["bit_errors"].mean()
            ),

        "max_bit_errors":
            int(
                group["bit_errors"].max()
            ),

        "avg_A":
            float(
                group["A"].mean()
            ),

        "avg_B":
            float(
                group["B"].mean()
            ),

        "avg_OP":
            float(
                group["OP"].mean()
            ),

        "A_ones_total":
            int(
                group["A"].map(
                    bit_count
                ).sum()
            ),

        "B_ones_total":
            int(
                group["B"].map(
                    bit_count
                ).sum()
            )
    }

    # --------------------------------------------------------
    # Operation-level features
    # --------------------------------------------------------

    for op_code, op_name in OPERATIONS.items():

        stats = calculate_operation_stats(
            group,
            op_code
        )

        signature[
            f"{op_name}_tests"
        ] = stats["tests"]

        signature[
            f"{op_name}_result_errors"
        ] = stats["result_errors"]

        signature[
            f"{op_name}_carry_errors"
        ] = stats["carry_errors"]

        signature[
            f"{op_name}_bit_errors"
        ] = stats["bit_errors"]

        signature[
            f"{op_name}_error_rate"
        ] = stats["error_rate"]

        signature[
            f"{op_name}_avg_bit_errors"
        ] = stats["avg_bit_errors"]

        signature[
            f"{op_name}_max_bit_errors"
        ] = stats["max_bit_errors"]

    # --------------------------------------------------------
    # Result bit errors
    # --------------------------------------------------------

    for bit in range(4):

        mask = 1 << bit

        expected_bit = (
            (
                group["expected_result"]
                .astype(int)
                & mask
            ) != 0
        )

        actual_bit = (
            (
                group["actual_result"]
                .astype(int)
                & mask
            ) != 0
        )

        signature[
            f"s{bit}_error_count"
        ] = int(
            (
                expected_bit
                != actual_bit
            ).sum()
        )

    # --------------------------------------------------------
    # Carry features
    # --------------------------------------------------------

    signature[
        "expected_carry_count"
    ] = int(
        group["expected_carry"].sum()
    )

    signature[
        "actual_carry_count"
    ] = int(
        group["actual_carry"].sum()
    )

    # Metadata
    signature["fault_id"] = fault_id
    signature["window_id"] = window_id
    signature["num_vectors"] = total_vectors

    return signature


# ============================================================
# 9. RAW DATA → SIGNATURES
# ============================================================

def raw_to_signatures(
    dataframe
):

    df = dataframe.copy()

    required = [

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

    missing = [
        c for c in required
        if c not in df.columns
    ]

    if missing:

        raise ValueError(
            "Missing columns: "
            + ", ".join(missing)
        )

    for column in required:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0).astype(int)

    if "fault_id" not in df.columns:

        df["fault_id"] = 0

    df["fault_id"] = pd.to_numeric(
        df["fault_id"],
        errors="coerce"
    ).fillna(0).astype(int)

    # Each fault contains 1024 vectors.
    df["vector_index"] = (
        df.groupby(
            "fault_id"
        ).cumcount()
    )

    df["window_id"] = (
        df["vector_index"]
        // 32
    )

    signatures = []

    for (
        fault_id,
        window_id
    ), group in df.groupby(
        ["fault_id", "window_id"],
        sort=True
    ):

        signatures.append(
            build_signature(
                group,
                fault_id,
                window_id
            )
        )

    return pd.DataFrame(
        signatures
    )


# ============================================================
# 10. PREPARE MODEL INPUT
# ============================================================

def prepare_features(
    signature
):

    data = pd.DataFrame(
        [signature]
    )

    missing = [
        f for f in MODEL_FEATURES
        if f not in data.columns
    ]

    if missing:

        raise ValueError(
            "Missing model features:\n"
            + "\n".join(missing)
        )

    X = data[
        MODEL_FEATURES
    ].copy()

    for column in X.columns:

        X[column] = pd.to_numeric(
            X[column],
            errors="coerce"
        ).fillna(0)

    return X


# ============================================================
# 11. AI DIAGNOSIS
# ============================================================

def diagnose(
    signature
):

    X = prepare_features(
        signature
    )

    prediction = int(
        MODEL.predict(X)[0]
    )

    if hasattr(
        MODEL,
        "predict_proba"
    ):

        probabilities = (
            MODEL.predict_proba(X)[0]
        )

        classes = [
            int(x)
            for x in MODEL.classes_
        ]

        probability_map = {
            cls: float(prob)
            for cls, prob
            in zip(
                classes,
                probabilities
            )
        }

    else:

        probability_map = {
            prediction: 1.0
        }

    confidence = (
        probability_map
        .get(
            prediction,
            0.0
        )
    )

    return (
        prediction,
        confidence,
        probability_map
    )


# ============================================================
# 12. DISPLAY DIAGNOSIS
# ============================================================

def display_diagnosis(
    prediction,
    confidence,
    probabilities,
    vectors
):

    info = FAULT_INFO[
        prediction
    ]

    st.markdown(
        "## AI Diagnosis"
    )

    col1, col2, col3, col4 = st.columns(
        4
    )

    col1.metric(
        "Predicted Fault",
        f"Fault #{prediction}"
    )

    col2.metric(
        "Operation",
        info["operation"]
    )

    col3.metric(
        "Confidence",
        f"{confidence * 100:.2f}%"
    )

    col4.metric(
        "Vectors",
        vectors
    )

    if confidence >= 0.90:

        box_class = "success-box"
        status = "HIGH-CONFIDENCE MATCH"

    elif confidence >= 0.60:

        box_class = "warning-box"
        status = "MODERATE-CONFIDENCE MATCH"

    else:

        box_class = "danger-box"
        status = "LOW-CONFIDENCE / AMBIGUOUS MATCH"

    st.markdown(
        f"""
        <div class="{box_class}">

        <b>{status}</b>

        <br><br>

        <b>Fault #{prediction} — {info["name"]}</b>

        <br>

        {info["description"]}

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Probability distribution
    # --------------------------------------------------------

    st.markdown(
        "### Fault Probability Distribution"
    )

    probability_data = []

    for fault_id in sorted(
        FAULT_INFO.keys()
    ):

        probability_data.append({

            "Fault":
                f"Fault #{fault_id}",

            "Probability":
                probabilities.get(
                    fault_id,
                    0
                ) * 100
        })

    probability_df = pd.DataFrame(
        probability_data
    )

    probability_df = (
        probability_df
        .sort_values(
            "Probability",
            ascending=False
        )
    )

    st.bar_chart(
        probability_df.set_index(
            "Fault"
        ),
        y="Probability",
        height=300
    )

    st.dataframe(
        probability_df.style.format(
            {
                "Probability":
                    "{:.2f}%"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 13. BEHAVIORAL SIGNATURE DISPLAY
# ============================================================

def display_signature(
    signature
):

    st.markdown(
        "## Behavioral Signature"
    )

    col1, col2, col3, col4, col5 = (
        st.columns(5)
    )

    col1.metric(
        "Result Errors",
        int(
            signature.get(
                "total_result_errors",
                0
            )
        )
    )

    col2.metric(
        "Carry Errors",
        int(
            signature.get(
                "total_carry_errors",
                0
            )
        )
    )

    col3.metric(
        "Bit Errors",
        int(
            signature.get(
                "total_bit_errors",
                0
            )
        )
    )

    col4.metric(
        "Error Vectors",
        int(
            signature.get(
                "error_vectors",
                0
            )
        )
    )

    col5.metric(
        "Error Rate",
        f"{float(signature.get('error_rate', 0)) * 100:.2f}%"
    )

    # ========================================================
    # OPERATION ANALYSIS
    # ========================================================

    st.markdown(
        "### Operation-Level Analysis"
    )

    rows = []

    for operation in [
        "ADD",
        "AND",
        "OR",
        "XOR"
    ]:

        rows.append({

            "Operation":
                operation,

            "Tests":
                int(
                    signature.get(
                        f"{operation}_tests",
                        0
                    )
                ),

            "Result Errors":
                int(
                    signature.get(
                        f"{operation}_result_errors",
                        0
                    )
                ),

            "Carry Errors":
                int(
                    signature.get(
                        f"{operation}_carry_errors",
                        0
                    )
                ),

            "Bit Errors":
                int(
                    signature.get(
                        f"{operation}_bit_errors",
                        0
                    )
                ),

            "Error Rate":
                float(
                    signature.get(
                        f"{operation}_error_rate",
                        0
                    )
                ) * 100
        })

    operation_df = pd.DataFrame(
        rows
    )

    st.dataframe(
        operation_df.style.format(
            {
                "Error Rate":
                    "{:.2f}%"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # BIT ANALYSIS
    # ========================================================

    st.markdown(
        "### Result Bit Error Analysis"
    )

    bit_df = pd.DataFrame({

        "Result Bit":
            [
                "s0",
                "s1",
                "s2",
                "s3"
            ],

        "Error Count":
            [
                int(
                    signature.get(
                        "s0_error_count",
                        0
                    )
                ),

                int(
                    signature.get(
                        "s1_error_count",
                        0
                    )
                ),

                int(
                    signature.get(
                        "s2_error_count",
                        0
                    )
                ),

                int(
                    signature.get(
                        "s3_error_count",
                        0
                    )
                )
            ]
    })

    if (
        bit_df["Error Count"]
        .sum()
        == 0
    ):

        st.success(
            "No result-bit errors detected. "
            "The observed failure is isolated "
            "to another path, such as carry."
        )

    else:

        st.bar_chart(
            bit_df.set_index(
                "Result Bit"
            ),
            y="Error Count",
            height=250
        )

    st.dataframe(
        bit_df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # CARRY ANALYSIS
    # ========================================================

    st.markdown(
        "### Carry Analysis"
    )

    expected_carry = int(
        signature.get(
            "expected_carry_count",
            0
        )
    )

    actual_carry = int(
        signature.get(
            "actual_carry_count",
            0
        )
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    col1.metric(
        "Expected Carry Count",
        expected_carry
    )

    col2.metric(
        "Actual Carry Count",
        actual_carry
    )

    col3.metric(
        "Carry Mismatch",
        abs(
            expected_carry
            -
            actual_carry
        )
    )


# ============================================================
# 14. AI EXPLANATION
# ============================================================

def display_explanation(
    signature,
    prediction,
    confidence
):

    info = FAULT_INFO[
        prediction
    ]

    operation = info[
        "operation"
    ]

    operation_error_rate = (
        float(
            signature.get(
                f"{operation}_error_rate",
                0
            )
        )
        * 100
    )

    st.markdown(
        "## AI Diagnosis Explanation"
    )

    st.markdown(
        f"""
        ### Why did the AI select Fault #{prediction}?

        The Random Forest compared the behavioral signature
        against patterns learned from the **six known RTL
        fault classes**.

        The strongest observed abnormality is associated
        with the **{operation}** operation.

        **Operation error rate:**
        {operation_error_rate:.2f}%

        **Observed signature:**

        - Result errors:
          {int(signature.get("total_result_errors", 0))}

        - Carry errors:
          {int(signature.get("total_carry_errors", 0))}

        - Bit errors:
          {int(signature.get("total_bit_errors", 0))}

        - Error vectors:
          {int(signature.get("error_vectors", 0))}

        **Most likely fault:**

        Fault #{prediction} —
        **{info["name"]}**

        **Model probability:**
        {confidence * 100:.2f}%
        """
    )

    st.info(
        "Important: confidence is the Random Forest "
        "class probability for this behavioral signature. "
        "It is NOT the same as overall model accuracy."
    )


# ============================================================
# 15. FEATURE IMPORTANCE
# ============================================================

def display_feature_importance():

    st.markdown(
        "## Important ML Features"
    )

    df = load_feature_importance()

    if df.empty:

        st.warning(
            "Feature importance file not found."
        )

        return

    if not {
        "Feature",
        "Importance"
    }.issubset(
        df.columns
    ):

        st.warning(
            "Unexpected feature importance format."
        )

        return

    df = df.copy()

    df["Importance"] = pd.to_numeric(
        df["Importance"],
        errors="coerce"
    ).fillna(0)

    top = df.head(
        10
    )

    st.dataframe(
        top.style.format(
            {
                "Importance":
                    "{:.4f}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        top.set_index(
            "Feature"
        ),
        y="Importance",
        height=350
    )


# ============================================================
# 16. MODEL PERFORMANCE PAGE
# ============================================================

def model_performance_page():

    st.header(
        "📊 Model Performance"
    )

    st.caption(
        "Final behavioral-signature classification model"
    )

    col1, col2, col3 = st.columns(
        3
    )

    col1.metric(
        "End-to-End Accuracy",
        "96.88%",
        "186 / 192"
    )

    col2.metric(
        "4-Fold Group CV",
        "95.31%",
        "mean accuracy"
    )

    col3.metric(
        "CV Std. Dev.",
        "2.27%",
        "four folds"
    )

    col1, col2, col3 = st.columns(
        3
    )

    col1.metric(
        "Training Signatures",
        "192",
        "32 windows × 6 faults"
    )

    col2.metric(
        "ML Features",
        "46"
    )

    col3.metric(
        "Random Forest",
        "500 Trees"
    )

    st.markdown(
        "### Validation Interpretation"
    )

    st.write(
        """
        The model was evaluated using group-based validation.
        Complete behavioral windows were kept together, so
        test windows were not mixed with training windows.

        This provides a stronger estimate of generalization
        to unseen behavioral windows than simply splitting
        individual rows at random.
        """
    )

    # --------------------------------------------------------
    # Fault-wise results
    # --------------------------------------------------------

    predictions = load_predictions()

    if not predictions.empty:

        actual_column = None
        predicted_column = None

        for column in predictions.columns:

            name = column.lower()

            if (
                actual_column is None
                and (
                    "actual" in name
                    or "true" in name
                )
            ):

                actual_column = column

            if (
                predicted_column is None
                and (
                    "predicted" in name
                    or "prediction" in name
                )
            ):

                predicted_column = column

        if (
            actual_column
            and predicted_column
        ):

            actual = pd.to_numeric(
                predictions[
                    actual_column
                ],
                errors="coerce"
            )

            predicted = pd.to_numeric(
                predictions[
                    predicted_column
                ],
                errors="coerce"
            )

            rows = []

            for fault_id in sorted(
                FAULT_INFO
            ):

                mask = (
                    actual
                    ==
                    fault_id
                )

                total = int(
                    mask.sum()
                )

                correct = int(
                    (
                        (
                            predicted
                            ==
                            fault_id
                        )
                        &
                        mask
                    ).sum()
                )

                accuracy = (
                    correct
                    /
                    total
                    *
                    100
                    if total
                    else 0
                )

                rows.append({

                    "Fault":
                        f"Fault #{fault_id}",

                    "Name":
                        FAULT_INFO[
                            fault_id
                        ]["name"],

                    "Correct":
                        correct,

                    "Total":
                        total,

                    "Accuracy":
                        accuracy
                })

            st.markdown(
                "### Fault-Wise Diagnosis"
            )

            st.dataframe(
                pd.DataFrame(
                    rows
                ).style.format(
                    {
                        "Accuracy":
                            "{:.2f}%"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # Feature importance
    # --------------------------------------------------------

    display_feature_importance()


# ============================================================
# 17. FAULT CATALOG
# ============================================================

def fault_catalog_page():

    st.header(
        "🧪 Six Deliberate RTL Faults"
    )

    rows = []

    for fault_id, info in (
        FAULT_INFO.items()
    ):

        rows.append({

            "Fault":
                f"Fault #{fault_id}",

            "Fault Name":
                info["name"],

            "Operation":
                info["operation"],

            "Injected Behavior":
                info["rtl"]
        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )

    for fault_id, info in (
        FAULT_INFO.items()
    ):

        with st.expander(
            f"Fault #{fault_id} — {info['name']}"
        ):

            st.write(
                f"**Affected operation:** "
                f"{info['operation']}"
            )

            st.write(
                f"**Description:** "
                f"{info['description']}"
            )

            st.code(
                info["rtl"],
                language="text"
            )


# ============================================================
# 18. SYSTEM ARCHITECTURE
# ============================================================

def architecture_page():

    st.header(
        "🏗️ System Architecture"
    )

    st.code(
        """
4-BIT ALU RTL
      |
      v
FAULT INJECTION
      |
      v
MASTER VERIFICATION
1024 INPUT VECTORS
      |
      v
EXPECTED vs ACTUAL OUTPUT
      |
      v
BEHAVIORAL SIGNATURE
192 WINDOWS
      |
      v
46 ML FEATURES
      |
      v
RANDOM FOREST
500 DECISION TREES
      |
      v
FAULT PREDICTION
FAULT #1 - #6
      |
      v
HUMAN-READABLE DIAGNOSIS
        """,
        language="text"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        "Fault Classes",
        "6"
    )

    col2.metric(
        "Verification Vectors",
        "1024"
    )

    col3.metric(
        "Behavioral Windows",
        "192"
    )

    col4.metric(
        "ML Features",
        "46"
    )

    st.markdown(
        "### Current Project Scope"
    )

    st.write(
        """
        The system converts RTL verification behavior into
        structured behavioral signatures and uses a Random
        Forest classifier to identify the closest learned
        fault pattern.

        This is a known-fault behavioral diagnosis
        proof-of-concept, not a universal detector for
        every possible RTL bug.
        """
    )

    st.markdown(
        "### Validated Results"
    )

    result_df = pd.DataFrame([

        {
            "Validation":
                "End-to-End",

            "Accuracy":
                "96.88%",

            "Details":
                "186 / 192 correct"
        },

        {
            "Validation":
                "4-Fold Group CV",

            "Accuracy":
                "95.31%",

            "Details":
                "Mean accuracy"
        },

        {
            "Validation":
                "CV Standard Deviation",

            "Accuracy":
                "2.27%",

            "Details":
                "Across four folds"
        }
    ])

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 19. SIDEBAR
# ============================================================

st.sidebar.title(
    "⚡ AI RTL Diagnostic"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Diagnosis Lab",
        "Model Performance",
        "Fault Catalog",
        "System Architecture"
    ]
)

st.sidebar.divider()

st.sidebar.write(
    "**Final Model:** "
    "Random Forest"
)

st.sidebar.write(
    "**Trees:** 500"
)

st.sidebar.write(
    "**ML Features:** 46"
)

st.sidebar.write(
    "**Fault Classes:** 6"
)

st.sidebar.divider()

st.sidebar.write(
    "End-to-End: **96.88%**"
)

st.sidebar.write(
    "Group CV: **95.31% ± 2.27%**"
)


# ============================================================
# 20. MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '⚡ AI-Assisted RTL Fault Diagnosis'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '4-bit ALU • Fault Injection • Behavioral Signatures • '
    'Random Forest • Human-Readable Diagnosis'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 21. DIAGNOSIS LAB
# ============================================================

if page == "Diagnosis Lab":

    st.header(
        "🔬 Diagnosis Lab"
    )

    mode = st.radio(
        "Diagnosis Mode",
        [
            "Known Fault Demonstration",
            "Upload New Verification Data"
        ],
        horizontal=True
    )

    # ========================================================
    # KNOWN FAULT DEMO
    # ========================================================

    if mode == "Known Fault Demonstration":

        signatures = load_signature_dataset()

        if signatures.empty:

            st.error(
                "dataset/fault_signatures.csv "
                "was not found."
            )

            st.stop()

        st.info(
            "Demonstration mode uses the six generated "
            "fault datasets. The hidden fault label is "
            "used only after prediction to verify whether "
            "the AI diagnosis is correct."
        )

        fault_id = st.selectbox(

            "Select RTL Fault",

            sorted(
                FAULT_INFO.keys()
            ),

            format_func=lambda x:
                (
                    f"Fault #{x} — "
                    f"{FAULT_INFO[x]['name']}"
                )
        )

        fault_data = signatures[
            pd.to_numeric(
                signatures["fault_id"],
                errors="coerce"
            )
            ==
            fault_id
        ].copy()

        windows = sorted(
            pd.to_numeric(
                fault_data["window_id"],
                errors="coerce"
            )
            .astype(int)
            .unique()
        )

        window_id = st.select_slider(

            "Behavioral Window",

            options=windows,

            value=windows[
                len(windows) // 2
            ]
        )

        selected = fault_data[
            pd.to_numeric(
                fault_data["window_id"],
                errors="coerce"
            )
            .astype(int)
            ==
            window_id
        ]

        if selected.empty:

            st.error(
                "Selected behavioral window "
                "was not found."
            )

            st.stop()

        signature = (
            selected.iloc[0]
            .to_dict()
        )

        vectors = int(
            signature.get(
                "num_vectors",
                32
            )
        )

        prediction, confidence, probabilities = (
            diagnose(
                signature
            )
        )

        st.markdown("---")

        display_diagnosis(
            prediction,
            confidence,
            probabilities,
            vectors
        )

        st.markdown("---")

        col1, col2, col3 = (
            st.columns(3)
        )

        col1.metric(
            "Behavioral Window",
            window_id
        )

        col2.metric(
            "Vectors",
            vectors
        )

        col3.metric(
            "Actual Hidden Fault",
            f"Fault #{fault_id}"
        )

        if prediction == fault_id:

            st.success(
                f"✅ CORRECT PREDICTION — "
                f"AI identified Fault #{prediction}."
            )

        else:

            st.error(
                f"❌ INCORRECT PREDICTION — "
                f"Actual Fault #{fault_id}, "
                f"AI predicted Fault #{prediction}."
            )

        st.markdown("---")

        display_signature(
            signature
        )

        st.markdown("---")

        display_explanation(
            signature,
            prediction,
            confidence
        )

        st.markdown("---")

        display_feature_importance()

    # ========================================================
    # UPLOAD / NEW DATA MODE
    # ========================================================

    else:

        st.subheader(
            "Diagnose New Verification Data"
        )

        st.write(
            """
            Upload either:

            • fault_signatures.csv

            or

            • raw fault_dataset.csv

            The application will convert raw verification
            vectors into behavioral signatures before
            passing them to the trained Random Forest.
            """
        )

        uploaded_file = st.file_uploader(
            "Upload CSV",
            type=["csv"]
        )

        if uploaded_file is None:

            st.info(
                "Upload a CSV file to begin diagnosis."
            )

        else:

            uploaded_df = pd.read_csv(
                uploaded_file
            )

            st.success(
                f"Loaded "
                f"{len(uploaded_df)} rows × "
                f"{len(uploaded_df.columns)} columns."
            )

            st.markdown(
                "### Uploaded Data Preview"
            )

            st.dataframe(
                uploaded_df.head(10),
                use_container_width=True,
                hide_index=True
            )

            try:

                # ------------------------------------------------
                # Already signature data?
                # ------------------------------------------------

                if all(
                    feature
                    in uploaded_df.columns
                    for feature
                    in MODEL_FEATURES
                ):

                    candidate_signatures = (
                        uploaded_df.copy()
                    )

                    if (
                        "window_id"
                        not in candidate_signatures.columns
                    ):

                        candidate_signatures[
                            "window_id"
                        ] = range(
                            len(
                                candidate_signatures
                            )
                        )

                # ------------------------------------------------
                # Otherwise raw verification data
                # ------------------------------------------------

                else:

                    candidate_signatures = (
                        raw_to_signatures(
                            uploaded_df
                        )
                    )

                if candidate_signatures.empty:

                    raise ValueError(
                        "No behavioral signatures "
                        "could be generated."
                    )

                st.markdown(
                    "### Generated Behavioral Signatures"
                )

                preview_columns = [

                    "fault_id",
                    "window_id",
                    "num_vectors",

                    "total_result_errors",
                    "total_carry_errors",
                    "total_bit_errors",

                    "error_rate"
                ]

                preview_columns = [
                    c
                    for c in preview_columns
                    if c in candidate_signatures.columns
                ]

                st.dataframe(
                    candidate_signatures[
                        preview_columns
                    ],
                    use_container_width=True,
                    hide_index=True
                )

                sample_index = st.selectbox(
                    "Select Signature",
                    range(
                        len(
                            candidate_signatures
                        )
                    )
                )

                signature = (
                    candidate_signatures
                    .iloc[
                        sample_index
                    ]
                    .to_dict()
                )

                vectors = int(
                    signature.get(
                        "num_vectors",
                        32
                    )
                )

                prediction, confidence, probabilities = (
                    diagnose(
                        signature
                    )
                )

                st.markdown("---")

                display_diagnosis(
                    prediction,
                    confidence,
                    probabilities,
                    vectors
                )

                st.markdown("---")

                display_signature(
                    signature
                )

                st.markdown("---")

                display_explanation(
                    signature,
                    prediction,
                    confidence
                )

                st.markdown("---")

                display_feature_importance()

                st.markdown("---")

                st.caption(
                    "If the uploaded data has no ground-truth "
                    "fault_id, the dashboard reports the closest "
                    "learned fault class but cannot claim whether "
                    "the prediction is correct."
                )

            except Exception as error:

                st.error(
                    "Unable to convert the uploaded data "
                    "into the 46-feature model input."
                )

                st.code(
                    str(error)
                )


# ============================================================
# 22. OTHER PAGES
# ============================================================

elif page == "Model Performance":

    model_performance_page()


elif page == "Fault Catalog":

    fault_catalog_page()


elif page == "System Architecture":

    architecture_page()