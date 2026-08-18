import streamlit as st
import pandas as pd
import joblib
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI RTL Fault Diagnosis",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

DATASET_FILE = "dataset/fault_dataset.csv"
MODEL_FILE = "outputs/final_model/final_random_forest.pkl"
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
# LOAD FILES
# ============================================================

@st.cache_resource
def load_model():

    return joblib.load(MODEL_FILE)


@st.cache_data
def load_dataset():

    return pd.read_csv(DATASET_FILE)


@st.cache_data
def load_features():

    feature_df = pd.read_csv(FEATURE_FILE)

    return feature_df["feature"].tolist()


# ============================================================
# FEATURE GENERATION
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
# LOAD DATA
# ============================================================

try:

    model = load_model()
    df = load_dataset()
    feature_list = load_features()

except Exception as e:

    st.error(
        f"Unable to load project files:\n\n{e}"
    )

    st.stop()


# ============================================================
# PREPARE DATASET
# ============================================================

df["vector_index"] = (
    df.groupby("fault_id").cumcount()
)

df["window_id"] = (
    df["vector_index"] // WINDOW_SIZE
)


# ============================================================
# HEADER
# ============================================================

st.title("⚡ AI RTL Fault Diagnosis System")

st.markdown(
    """
    ### AI-Assisted RTL Verification & Bug Diagnosis

    This system analyzes behavioral signatures generated from
    RTL verification results and uses a trained Random Forest
    classifier to identify the most likely RTL fault.
    """
)

st.divider()


# ============================================================
# PROJECT STATUS
# ============================================================

st.subheader("System Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Verification Vectors",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Behavioral Windows",
        "32"
    )

with col3:
    st.metric(
        "ML Features",
        len(feature_list)
    )

with col4:
    st.metric(
        "Fault Classes",
        "6"
    )


st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Diagnosis Controls")

st.sidebar.markdown(
    "Select a fault dataset and behavioral window."
)


fault_options = sorted(
    df["fault_id"].unique()
)

fault_labels = [
    f"Fault #{fault_id} - {FAULT_INFO[int(fault_id)]['name']}"
    for fault_id in fault_options
]

selected_label = st.sidebar.selectbox(
    "Fault Dataset",
    fault_labels
)

selected_fault = int(
    selected_label.split("#")[1].split(" ")[0]
)


fault_data = df[
    df["fault_id"] == selected_fault
].copy()


available_windows = sorted(
    fault_data["window_id"].unique()
)


selected_window = st.sidebar.selectbox(
    "Behavioral Window",
    available_windows
)


run_diagnosis = st.sidebar.button(
    "🔍 RUN AI DIAGNOSIS",
    use_container_width=True
)


# ============================================================
# SELECTED WINDOW INFORMATION
# ============================================================

window = fault_data[
    fault_data["window_id"] == selected_window
].copy()


signature = create_signature(window)


# ============================================================
# WINDOW OVERVIEW
# ============================================================

st.subheader("Behavioral Window")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Fault Dataset",
        f"Fault #{selected_fault}"
    )

with col2:

    st.metric(
        "Window ID",
        selected_window
    )

with col3:

    st.metric(
        "Vectors",
        len(window)
    )


# ============================================================
# RUN DIAGNOSIS
# ============================================================

if run_diagnosis:

    signature_df = pd.DataFrame(
        [signature]
    )

    missing_features = [
        feature
        for feature in feature_list
        if feature not in signature_df.columns
    ]

    if missing_features:

        st.error(
            "Feature mismatch detected."
        )

        st.write(
            missing_features
        )

        st.stop()

    X = signature_df[
        feature_list
    ].copy()

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = model.predict(X)[0]

    probabilities = model.predict_proba(X)[0]

    classes = model.classes_

    confidence = (
        probabilities[
            list(classes).index(prediction)
        ] * 100
    )

    info = FAULT_INFO[int(prediction)]

    # ========================================================
    # DIAGNOSIS RESULT
    # ========================================================

    st.divider()

    st.subheader("🤖 AI Diagnosis")

    if int(prediction) == selected_fault:

        st.success(
            "✅ AI prediction matches the actual hidden fault."
        )

    else:

        st.warning(
            "⚠️ AI prediction does not match the selected fault."
        )


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Predicted Fault",
            f"#{prediction}"
        )

    with col2:

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

    with col3:

        st.metric(
            "Affected Operation",
            info["operation"]
        )


    st.info(
        f"**{info['name']}**\n\n"
        f"{info['description']}"
    )


    # ========================================================
    # PROBABILITY DISTRIBUTION
    # ========================================================

    st.subheader("📊 Fault Probability Distribution")

    probability_data = pd.DataFrame({

        "Fault":
            [
                f"Fault #{fault}"
                for fault in classes
            ],

        "Probability":
            [
                probability * 100
                for probability in probabilities
            ]
    })

    probability_data = (
        probability_data
        .sort_values(
            "Probability",
            ascending=False
        )
    )

    st.bar_chart(
        probability_data.set_index("Fault")
    )


    # ========================================================
    # BEHAVIORAL SIGNATURE
    # ========================================================

    st.subheader("🔬 Behavioral Signature")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Result Errors",
            int(signature["total_result_errors"])
        )

    with col2:

        st.metric(
            "Carry Errors",
            int(signature["total_carry_errors"])
        )

    with col3:

        st.metric(
            "Bit Errors",
            int(signature["total_bit_errors"])
        )

    with col4:

        st.metric(
            "Error Vectors",
            int(signature["error_vectors"])
        )


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Error Rate",
            f"{signature['error_rate']:.4f}"
        )

    with col2:

        st.metric(
            "Average Bit Errors",
            f"{signature['avg_bit_errors']:.4f}"
        )

    with col3:

        st.metric(
            "Maximum Bit Errors",
            int(signature["max_bit_errors"])
        )


    # ========================================================
    # OPERATION ERROR SUMMARY
    # ========================================================

    st.subheader("⚙️ Operation Error Summary")

    operation_table = []

    for prefix in [
        "ADD",
        "AND",
        "OR",
        "XOR"
    ]:

        operation_table.append({

            "Operation":
                prefix,

            "Tests":
                signature[
                    f"{prefix}_tests"
                ],

            "Result Errors":
                signature[
                    f"{prefix}_result_errors"
                ],

            "Carry Errors":
                signature[
                    f"{prefix}_carry_errors"
                ],

            "Bit Errors":
                signature[
                    f"{prefix}_bit_errors"
                ],

            "Error Rate":
                round(
                    signature[
                        f"{prefix}_error_rate"
                    ],
                    4
                )
        })


    operation_df = pd.DataFrame(
        operation_table
    )

    st.dataframe(
        operation_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # BIT ERROR SUMMARY
    # ========================================================

    st.subheader("🔢 Result Bit Error Summary")

    bit_data = pd.DataFrame({

        "Bit":
            [
                "s0",
                "s1",
                "s2",
                "s3"
            ],

        "Error Count":
            [
                signature["s0_error_count"],
                signature["s1_error_count"],
                signature["s2_error_count"],
                signature["s3_error_count"]
            ]
    })

    st.dataframe(
        bit_data,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # VERIFICATION RESULT
    # ========================================================

    st.divider()

    st.subheader("🎯 Prediction Verification")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Actual hidden fault:** "
            f"Fault #{selected_fault}"
        )

    with col2:

        st.write(
            f"**AI predicted fault:** "
            f"Fault #{prediction}"
        )


    if int(prediction) == selected_fault:

        st.success(
            "RESULT: CORRECT PREDICTION"
        )

    else:

        st.error(
            "RESULT: INCORRECT PREDICTION"
        )


    # ========================================================
    # RAW WINDOW DATA
    # ========================================================

    with st.expander(
        "🔍 View Raw Verification Vectors"
    ):

        display_columns = [
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

        st.dataframe(
            window[display_columns],
            use_container_width=True,
            hide_index=True
        )


else:

    # ========================================================
    # INITIAL STATE
    # ========================================================

    st.info(
        "Select a fault dataset and behavioral window "
        "from the sidebar, then click **RUN AI DIAGNOSIS**."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI-Assisted RTL Verification & Bug Diagnosis | "
    "Random Forest | 46 Behavioral Features | "
    "6 RTL Fault Classes"
)