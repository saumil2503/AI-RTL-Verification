from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether
)

# ============================================================
# AI-ASSISTED RTL VERIFICATION & FAULT DIAGNOSIS
# DETAILED PROJECT REPORT GENERATOR
# ============================================================

OUTPUT_FILE = "AI_RTL_Verification_Detailed_Project_Report.pdf"

# ============================================================
# DOCUMENT
# ============================================================

doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=1.6 * cm,
    leftMargin=1.6 * cm,
    topMargin=1.6 * cm,
    bottomMargin=1.6 * cm
)

# ============================================================
# STYLES
# ============================================================

styles = getSampleStyleSheet()

styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=15
    )
)

styles.add(
    ParagraphStyle(
        name="CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=17,
        alignment=TA_CENTER,
        spaceAfter=12
    )
)

styles.add(
    ParagraphStyle(
        name="Chapter",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        spaceBefore=10,
        spaceAfter=10,
        textColor=HexColor("#17365D")
    )
)

styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        spaceBefore=9,
        spaceAfter=6,
        textColor=HexColor("#1F4E79")
    )
)

styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        spaceAfter=7
    )
)

styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        spaceAfter=5
    )
)

styles.add(
    ParagraphStyle(
        name="MyCode",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=10,
        leftIndent=8,
        rightIndent=8,
        spaceBefore=5,
        spaceAfter=8
    )
)

styles.add(
    ParagraphStyle(
        name="Important",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=15,
        leftIndent=10,
        rightIndent=10,
        spaceBefore=6,
        spaceAfter=8,
        textColor=HexColor("#17365D")
    )
)

styles.add(
    ParagraphStyle(
        name="Center",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        spaceAfter=6
    )
)

# ============================================================
# HELPERS
# ============================================================

story = []


def P(text, style="Body"):
    story.append(Paragraph(text, styles[style]))


def H1(text):
    story.append(Paragraph(text, styles["Chapter"]))


def H2(text):
    story.append(Paragraph(text, styles["Section"]))


def spacer(height=0.25):
    story.append(Spacer(1, height * cm))


def new_page():
    story.append(PageBreak())


def make_table(data, widths, font_size=8):
    table = Table(
        data,
        colWidths=widths,
        repeatRows=1
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HexColor("#D9EAF7")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    HexColor("#17365D")
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    font_size
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
            ]
        )
    )

    story.append(table)
    spacer(0.3)


def code_block(text):
    story.append(
        Paragraph(
            text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>"),
            styles["Code"]
        )
    )


def bullet(text):
    P("• " + text)


def numbered(number, text):
    P(f"<b>{number}.</b> {text}")


# ============================================================
# COVER PAGE
# ============================================================

spacer(2)

P(
    "AI-ASSISTED RTL VERIFICATION<br/>"
    "&amp; FAULT DIAGNOSIS",
    "CoverTitle"
)

P(
    "End-to-End VLSI / RTL Verification Project<br/>"
    "with Custom Dataset Generation and Machine Learning",
    "CoverSubtitle"
)

spacer(1)

P(
    "<b>Detailed Technical Project Report</b>",
    "Center"
)

spacer(1)

make_table(
    [
        ["Project Component", "Implementation"],
        ["RTL Design", "4-bit Arithmetic Logic Unit"],
        ["Fault Injection", "6 intentionally faulty RTL implementations"],
        ["Verification", "SystemVerilog"],
        ["Simulation", "Xilinx Vivado / XSim"],
        ["Raw Dataset", "6,144 verification observations"],
        ["Behavioral Windows", "192 signatures"],
        ["ML Features", "46 behavioral features"],
        ["Machine Learning", "Random Forest"],
        ["Validation", "4-fold Group Cross-Validation"],
        ["Application", "Streamlit Dashboard"],
    ],
    [6 * cm, 10 * cm]
)

spacer(1)

P(
    "<b>Purpose:</b> To demonstrate how RTL verification data can be converted "
    "into behavioral signatures and used by machine learning to automatically "
    "diagnose the likely underlying RTL implementation fault.",
    "Important"
)

P(
    "<b>Important scope note:</b> The completed implementation does not contain "
    "an IoT subsystem. The final project is an AI-assisted RTL verification and "
    "fault-diagnosis system with a Streamlit software dashboard.",
    "Important"
)

new_page()

# ============================================================
# TABLE OF CONTENTS
# ============================================================

H1("Table of Contents")

toc = [
    ["1", "Project Abstract"],
    ["2", "Introduction"],
    ["3", "Problem Statement"],
    ["4", "Project Objectives"],
    ["5", "Technology Stack"],
    ["6", "Overall System Architecture"],
    ["7", "4-bit ALU Fundamentals"],
    ["8", "Golden RTL Design"],
    ["9", "Fault Injection"],
    ["10", "Detailed Fault Classes"],
    ["11", "SystemVerilog Verification"],
    ["12", "Vivado/XSim Simulation"],
    ["13", "Custom Dataset Generation"],
    ["14", "Raw Dataset Structure"],
    ["15", "Dataset Statistics"],
    ["16", "Behavioral Windows"],
    ["17", "Behavioral Signatures"],
    ["18", "Feature Engineering"],
    ["19", "The 46 ML Features"],
    ["20", "Why Machine Learning?"],
    ["21", "ML Model Experiments"],
    ["22", "Random Forest"],
    ["23", "Training"],
    ["24", "Group Cross-Validation"],
    ["25", "Hyperparameter Tuning"],
    ["26", "Feature Importance"],
    ["27", "Misclassification Analysis"],
    ["28", "Hierarchical Diagnosis"],
    ["29", "Final Model"],
    ["30", "Real-Time Diagnosis"],
    ["31", "Streamlit Dashboard"],
    ["32", "IoT Clarification"],
    ["33", "Complete End-to-End Workflow"],
    ["34", "Results"],
    ["35", "Limitations"],
    ["36", "Future Improvements"],
    ["37", "Interview Explanation"],
    ["38", "Conclusion"],
]

make_table(
    [["Chapter", "Topic"]] + toc,
    [2.5 * cm, 13.5 * cm],
    8
)

new_page()

# ============================================================
# 1 ABSTRACT
# ============================================================

H1("1. Project Abstract")

P(
    "RTL verification is one of the most important stages in digital IC and "
    "ASIC development. A verification environment can identify whether the "
    "observed output of an RTL implementation matches the expected behavior. "
    "However, a traditional pass/fail result does not necessarily explain "
    "which implementation fault produced the failure."
)

P(
    "This project extends RTL verification by adding a machine-learning-based "
    "fault diagnosis layer. A 4-bit ALU is used as the base RTL design. "
    "Six intentionally faulty versions of the ALU are created. A SystemVerilog "
    "verification environment executes the designs in Xilinx Vivado/XSim and "
    "compares actual outputs with golden expected outputs."
)

P(
    "Instead of using an external machine-learning dataset, the project creates "
    "its own dataset directly from RTL simulation results. The verification "
    "environment produces 6,144 raw observations. These observations are then "
    "grouped into 192 behavioral windows and converted into 46 numerical "
    "behavioral features."
)

P(
    "Several machine-learning models are evaluated, including Decision Tree, "
    "Random Forest and SVM. Group-based validation is used to prevent vectors "
    "belonging to the same behavioral window from appearing in both training "
    "and testing data."
)

P(
    "The final system uses a Random Forest classifier. The trained model receives "
    "a behavioral signature and predicts the most likely RTL fault class. "
    "A Streamlit application provides an interactive interface for displaying "
    "the diagnosis."
)

P(
    "<b>The major idea of the project is therefore:</b> use the behavioral "
    "fingerprint produced by RTL verification as the input to an AI-based "
    "fault-diagnosis system."
)

new_page()

# ============================================================
# 2 INTRODUCTION
# ============================================================

H1("2. Introduction")

H2("2.1 What is RTL?")

P(
    "RTL stands for Register Transfer Level. It is a hardware description "
    "abstraction used to describe how digital information moves between "
    "registers and how combinational logic transforms that information."
)

P(
    "Languages such as Verilog and SystemVerilog are commonly used to describe "
    "RTL. The RTL description can later be synthesized into gates and "
    "implemented on an FPGA or fabricated as part of an ASIC."
)

H2("2.2 What is RTL Verification?")

P(
    "RTL verification checks whether the hardware implementation behaves "
    "according to its intended specification. A verification environment "
    "generates inputs, applies them to the design under test, observes outputs "
    "and compares those outputs against expected results."
)

P(
    "For this project, the expected behavior is generated from the golden "
    "4-bit ALU specification. The faulty implementations are then tested "
    "against this reference."
)

H2("2.3 Why Fault Diagnosis?")

P(
    "Suppose a testbench detects that an ALU produces an incorrect output. "
    "The verification engineer knows that something is wrong, but a failure "
    "alone does not necessarily identify the root cause."
)

P(
    "Different RTL bugs can produce different patterns of errors. One fault "
    "may affect only carry during addition, while another may affect multiple "
    "result bits during AND operations. These patterns can be treated as "
    "behavioral signatures."
)

P(
    "The project investigates whether machine learning can recognize those "
    "signatures automatically."
)

H2("2.4 Core Research Question")

P(
    "<b>Can RTL verification behavior be converted into a feature vector "
    "that allows a machine-learning model to identify the underlying injected "
    "RTL fault?</b>"
)

new_page()

# ============================================================
# 3 PROBLEM STATEMENT
# ============================================================

H1("3. Problem Statement")

P(
    "Traditional verification primarily answers the question: "
    "<b>Does the RTL implementation behave correctly?</b>"
)

P(
    "This project adds another question:"
)

P(
    "<b>What type of RTL implementation fault is most likely responsible "
    "for the observed behavioral failure pattern?</b>",
    "Important"
)

P(
    "The problem is formulated as a supervised classification task."
)

make_table(
    [
        ["Element", "Meaning"],
        ["Input", "Behavioral signature containing 46 features"],
        ["Output", "Fault class from 1 to 6"],
        ["Classes", "Six intentionally injected RTL faults"],
        ["Training data", "192 generated behavioral signatures"],
        ["Classifier", "Random Forest"],
    ],
    [5 * cm, 11 * cm]
)

H2("3.1 Why Use a Custom Dataset?")

P(
    "A major feature of this project is that the dataset is not taken from "
    "a generic machine-learning repository. The data must describe specific "
    "RTL behavior, so it is generated directly from the verification environment."
)

P(
    "This makes the dataset highly relevant to the actual hardware problem. "
    "Every row corresponds to a real simulation observation and every target "
    "label corresponds to the RTL fault that generated that observation."
)

H2("3.2 Supervised Learning Formulation")

P(
    "For supervised learning, the training data contains both the input "
    "behavioral measurements and the known fault label. During training, "
    "the Random Forest learns statistical relationships between the features "
    "and fault classes."
)

P(
    "During diagnosis, the fault label is not supplied to the classifier. "
    "Only the behavioral signature is supplied."
)

new_page()

# ============================================================
# 4 OBJECTIVES
# ============================================================

H1("4. Project Objectives")

numbered(
    1,
    "Design a simple reference 4-bit ALU in RTL."
)

numbered(
    2,
    "Create multiple faulty RTL implementations using controlled fault injection."
)

numbered(
    3,
    "Develop a SystemVerilog verification environment capable of exercising the ALU."
)

numbered(
    4,
    "Compare expected and actual result/carry behavior."
)

numbered(
    5,
    "Generate a custom verification dataset automatically."
)

numbered(
    6,
    "Group vector-level observations into behavioral windows."
)

numbered(
    7,
    "Generate behavioral signatures from each window."
)

numbered(
    8,
    "Extract 46 meaningful ML features."
)

numbered(
    9,
    "Train and compare multiple machine-learning classifiers."
)

numbered(
    10,
    "Evaluate models using group-based cross-validation."
)

numbered(
    11,
    "Analyze feature importance and fault confusion."
)

numbered(
    12,
    "Tune the Random Forest model."
)

numbered(
    13,
    "Train a final model using the complete signature dataset."
)

numbered(
    14,
    "Build a diagnosis engine that predicts an RTL fault from a behavioral window."
)

numbered(
    15,
    "Expose the final system through a Streamlit dashboard."
)

H2("4.1 Learning Objectives")

P(
    "The project also provides practical experience across multiple engineering "
    "domains: digital logic, Verilog/SystemVerilog, RTL verification, simulation, "
    "Python data processing, machine learning, model evaluation, and application "
    "development."
)

P(
    "This makes the project interdisciplinary rather than being only an RTL "
    "design project or only a machine-learning project."
)

new_page()

# ============================================================
# 5 TECHNOLOGY STACK
# ============================================================

H1("5. Technology Stack")

make_table(
    [
        ["Technology", "Role in Project"],
        ["Verilog", "RTL implementation of ALU and faulty variants"],
        ["SystemVerilog", "Verification testbench and dataset generation"],
        ["Vivado", "RTL project and simulation environment"],
        ["XSim", "Behavioral simulation"],
        ["Python", "Dataset analysis, ML and diagnosis"],
        ["Pandas", "Dataset manipulation and feature processing"],
        ["Scikit-learn", "Machine-learning models"],
        ["Joblib", "Saving/loading trained Random Forest"],
        ["Streamlit", "Interactive dashboard"],
        ["CSV", "Dataset and ML-result storage"],
        ["Git/GitHub", "Project version control and repository hosting"],
    ],
    [4 * cm, 12 * cm]
)

H2("5.1 Software Architecture")

P(
    "The project is divided into several logical layers."
)

make_table(
    [
        ["Layer", "Purpose"],
        ["RTL Layer", "Golden ALU and faulty ALU implementations"],
        ["Verification Layer", "SystemVerilog testbench"],
        ["Simulation Layer", "Vivado/XSim execution"],
        ["Dataset Layer", "Raw vectors and behavioral signatures"],
        ["ML Layer", "Feature engineering and classification"],
        ["Diagnosis Layer", "Runtime fault prediction"],
        ["Application Layer", "Streamlit dashboard"],
    ],
    [5 * cm, 11 * cm]
)

H2("5.2 Project Directory")

code_block(
"""AI_RTL_Verification/
|
|-- rtl/
|   |-- alu.v
|   |-- alu_faulty.v
|   |-- alu_fault2.v
|   |-- alu_fault3.v
|   |-- alu_fault4.v
|   |-- alu_fault5.v
|   |-- alu_fault6.v
|
|-- tb/
|   |-- new_verification_tb.sv
|
|-- dataset/
|   |-- fault_dataset.csv
|   |-- fault_signatures.csv
|   |-- ml_features.csv
|
|-- ml/
|   |-- feature_engineering.py
|   |-- build_fault_signatures.py
|   |-- cross_validate_model.py
|   |-- tune_signature_model.py
|   |-- final_train_model.py
|   |-- real_time_diagnosis.py
|
|-- outputs/
|   |-- final_model/
|   |-- signature_models/
|
|-- app.py
|-- requirements.txt
|-- README.md"""
)

new_page()

# ============================================================
# 6 ARCHITECTURE
# ============================================================

H1("6. Overall System Architecture")

P(
    "The complete project can be understood as a sequence of transformations."
)

P(
    "<b>Step 1:</b> RTL is created.<br/>"
    "<b>Step 2:</b> Controlled faults are injected.<br/>"
    "<b>Step 3:</b> SystemVerilog generates verification vectors.<br/>"
    "<b>Step 4:</b> Vivado/XSim simulates the designs.<br/>"
    "<b>Step 5:</b> Expected and actual outputs are compared.<br/>"
    "<b>Step 6:</b> Raw observations are stored as a dataset.<br/>"
    "<b>Step 7:</b> Observations are grouped into behavioral windows.<br/>"
    "<b>Step 8:</b> Each window is converted into a 46-feature behavioral signature.<br/>"
    "<b>Step 9:</b> Random Forest learns fault patterns.<br/>"
    "<b>Step 10:</b> New behavioral signatures are classified.<br/>"
    "<b>Step 11:</b> Streamlit displays the diagnosis."
)

P(
    "Conceptually:"
)

P(
    "<b>Hardware behavior → verification evidence → numerical representation → "
    "machine learning → fault diagnosis</b>",
    "Important"
)

H2("6.1 Why This Architecture Is Useful")

P(
    "The important engineering principle is that the AI layer does not directly "
    "modify or replace the RTL verification environment. The verification "
    "environment remains responsible for determining actual versus expected "
    "behavior."
)

P(
    "Machine learning is placed above the verification layer. Its job is to "
    "interpret the accumulated behavioral evidence and estimate which known "
    "fault class best explains that evidence."
)

new_page()

# ============================================================
# 7 ALU
# ============================================================

H1("7. 4-bit ALU Fundamentals")

P(
    "The Arithmetic Logic Unit is the central hardware design used for the project. "
    "A 4-bit ALU is small enough to make simulation and analysis manageable while "
    "still providing multiple independent operations and meaningful fault patterns."
)

H2("7.1 Inputs")

make_table(
    [
        ["Signal", "Width", "Description"],
        ["A", "4 bits", "First operand"],
        ["B", "4 bits", "Second operand"],
        ["OP", "2 bits", "Operation selector"],
    ],
    [3 * cm, 3 * cm, 10 * cm]
)

H2("7.2 Outputs")

make_table(
    [
        ["Signal", "Width", "Description"],
        ["RESULT", "4 bits", "ALU operation result"],
        ["CARRY", "1 bit", "Carry generated during addition"],
    ],
    [3 * cm, 3 * cm, 10 * cm]
)

H2("7.3 Operation Table")

make_table(
    [
        ["OP", "Operation", "Equation"],
        ["00", "ADD", "RESULT = A + B"],
        ["01", "AND", "RESULT = A & B"],
        ["10", "OR", "RESULT = A | B"],
        ["11", "XOR", "RESULT = A ^ B"],
    ],
    [2.5 * cm, 4 * cm, 9.5 * cm]
)

H2("7.4 Addition Example")

P(
    "For example, if A = 15 and B = 12:"
)

code_block(
"""15 + 12 = 27
27 decimal = 11011 binary

RESULT = 1011
CARRY  = 1"""
)

P(
    "The 4-bit result contains the lower four bits while the fifth bit becomes "
    "the carry output."
)

H2("7.5 Why the ALU Is Suitable")

P(
    "The four operations produce different behavioral patterns. Therefore, "
    "a fault affecting one operation can be detected by selectively exercising "
    "that operation and comparing the observed output with the golden reference."
)

new_page()

# ============================================================
# 8 GOLDEN RTL
# ============================================================

H1("8. Golden RTL Design")

P(
    "The golden ALU represents the expected correct behavior. It is used as the "
    "reference against which the faulty implementations are evaluated."
)

P(
    "The verification environment effectively performs:"
)

code_block(
"""expected_result = Golden_ALU(A, B, OP)

actual_result = Faulty_ALU(A, B, OP)

result_error = (expected_result != actual_result)

carry_error = (expected_carry != actual_carry)"""
)

H2("8.1 Golden Reference Concept")

P(
    "The golden model is important because machine learning cannot determine "
    "whether an output is correct by itself. The verification system first "
    "establishes what the correct output should be."
)

P(
    "The AI layer therefore depends on the quality of the verification evidence."
)

H2("8.2 Expected vs Actual")

make_table(
    [
        ["Condition", "Interpretation"],
        ["Expected = Actual", "Vector passes"],
        ["Expected ≠ Actual", "Result error"],
        ["Expected carry ≠ Actual carry", "Carry error"],
        ["Multiple result bits differ", "Higher bit-error count"],
    ],
    [7 * cm, 9 * cm]
)

H2("8.3 Bit-Level Comparison")

P(
    "The project also calculates how many individual result bits differ. "
    "This is more informative than a simple pass/fail flag because two faulty "
    "outputs can differ by one bit or by all four bits."
)

P(
    "This bit-level information becomes one of the important behavioral signals "
    "used by the ML model."
)

new_page()

# ============================================================
# 9 FAULT INJECTION
# ============================================================

H1("9. Fault Injection")

P(
    "Fault injection means deliberately modifying an otherwise correct RTL "
    "implementation so that it behaves incorrectly in a controlled and known way."
)

P(
    "In this project, fault injection is essential because the machine-learning "
    "dataset requires known target labels. If a simulation produces a failure "
    "and we know which injected fault generated it, the observation can be used "
    "as a supervised training example."
)

H2("9.1 Fault Injection Process")

numbered(1, "Create a correct golden ALU.")
numbered(2, "Duplicate the design into faulty versions.")
numbered(3, "Introduce one intentional implementation error per faulty module.")
numbered(4, "Compile all variants with the verification environment.")
numbered(5, "Apply identical test behavior to every variant.")
numbered(6, "Record expected and actual results.")
numbered(7, "Assign the corresponding fault_id.")

H2("9.2 Why Multiple Faults?")

P(
    "A single fault would only create a binary classification problem. Six faults "
    "make the problem more realistic because the classifier must distinguish "
    "between several behavioral patterns."
)

H2("9.3 Fault Classes")

make_table(
    [
        ["ID", "Fault"],
        ["1", "ADD Carry Fault"],
        ["2", "AND-to-OR Logic Fault"],
        ["3", "XOR-to-XNOR Logic Fault"],
        ["4", "OR-to-XOR Logic Fault"],
        ["5", "Opcode Selection Fault"],
        ["6", "Inverted B Operand Fault"],
    ],
    [3 * cm, 13 * cm]
)

new_page()

# ============================================================
# 10 DETAILED FAULTS
# ============================================================

H1("10. Detailed Fault Classes")

H2("10.1 Fault #1 — ADD Carry Fault")

P(
    "The first faulty implementation intentionally prevents the ADD operation "
    "from producing the correct carry output."
)

P(
    "The result may still be numerically correct for many vectors, but the carry "
    "output becomes incorrect when the addition generates a carry."
)

P(
    "This creates a behavioral signature dominated by carry mismatches rather "
    "than result-bit mismatches."
)

H2("10.2 Fault #2 — AND-to-OR Logic Fault")

P(
    "The AND operation is intentionally replaced with OR behavior."
)

code_block(
"""Correct:
RESULT = A & B

Faulty:
RESULT = A | B"""
)

P(
    "Whenever A & B differs from A | B, the result becomes incorrect. "
    "This produces result and bit-level errors concentrated around AND tests."
)

H2("10.3 Fault #3 — XOR-to-XNOR Logic Fault")

P(
    "The XOR operation is intentionally replaced by its complement, XNOR."
)

code_block(
"""Correct:
RESULT = A ^ B

Faulty:
RESULT = ~(A ^ B)"""
)

P(
    "Because XNOR is the inverse of XOR for each result bit, this fault can "
    "produce strong bit-level error signatures."
)

H2("10.4 Fault #4 — OR-to-XOR Logic Fault")

P(
    "The OR operation is intentionally implemented as XOR."
)

code_block(
"""Correct:
RESULT = A | B

Faulty:
RESULT = A ^ B"""
)

P(
    "The two operations are identical for some input combinations but differ "
    "when both operands contain a logic 1 in the same bit position. This explains "
    "why the fault does not necessarily fail every OR vector."
)

new_page()

H2("10.5 Fault #5 — Opcode Selection Fault")

P(
    "The fifth fault changes the operation-selection logic. Instead of mapping "
    "opcode 10 to OR, the faulty implementation selects AND."
)

code_block(
"""Correct:
OP = 10  -> OR

Faulty:
OP = 10  -> AND"""
)

P(
    "This is different from simply changing an operator because the problem is "
    "located in the control/opcode-selection path."
)

H2("10.6 Fault #6 — Inverted B Operand Fault")

P(
    "The sixth fault uses the inverted value of B for the AND operation."
)

code_block(
"""Correct:
RESULT = A & B

Faulty:
RESULT = A & ~B"""
)

P(
    "This creates a characteristic pattern in which the AND operation produces "
    "incorrect result bits based on the complement of B."
)

H2("10.7 Why the Faults Can Be Confused")

P(
    "Some faults produce overlapping signatures. For example, Fault #2 and "
    "Fault #6 both affect AND behavior. Fault #4 and Fault #5 can also produce "
    "related OR-operation error patterns."
)

P(
    "This is one of the most important reasons why the project uses an entire "
    "behavioral window instead of attempting diagnosis from one test vector."
)

new_page()

# ============================================================
# 11 SYSTEMVERILOG
# ============================================================

H1("11. SystemVerilog Verification")

P(
    "SystemVerilog is used to construct the verification environment around "
    "the faulty ALU implementations."
)

H2("11.1 Verification Responsibilities")

bullet("Generate operand combinations.")
bullet("Select the ALU operation.")
bullet("Calculate the expected result.")
bullet("Calculate the expected carry.")
bullet("Observe the actual result.")
bullet("Observe the actual carry.")
bullet("Compare expected and actual behavior.")
bullet("Calculate bit-level differences.")
bullet("Store the verification information.")

H2("11.2 Result Error")

P(
    "The result error is a binary indicator:"
)

code_block(
"""result_error = 1
if expected_result != actual_result"""
)

H2("11.3 Carry Error")

P(
    "Similarly:"
)

code_block(
"""carry_error = 1
if expected_carry != actual_carry"""
)

H2("11.4 Bit Errors")

P(
    "The result bits are compared individually. For a 4-bit result, the number "
    "of mismatching bit positions ranges from zero to four."
)

P(
    "This gives the ML pipeline more information than a simple result_error flag."
)

H2("11.5 Dataset Generation")

P(
    "The verification testbench was extended beyond ordinary checking. It "
    "generates the structured behavioral dataset needed by the Python ML stage."
)

new_page()

# ============================================================
# 12 VIVADO
# ============================================================

H1("12. Vivado / XSim Simulation")

P(
    "Xilinx Vivado is used as the hardware-development and simulation environment. "
    "XSim executes the SystemVerilog verification environment."
)

H2("12.1 Simulation Flow")

code_block(
"""RTL files
   |
   v
SystemVerilog Testbench
   |
   v
Vivado Compilation
   |
   v
XSim Elaboration
   |
   v
Behavioral Simulation
   |
   v
Verification Results
   |
   v
CSV Dataset"""
)

H2("12.2 Final Dataset Generation Result")

make_table(
    [
        ["Parameter", "Value"],
        ["Fault classes", "6"],
        ["Behavioral windows", "32"],
        ["Vectors per window", "32"],
        ["Vectors per fault", "1024"],
        ["Total CSV rows", "6144"],
    ],
    [7 * cm, 9 * cm]
)

P(
    "The final simulation successfully generated the dataset file:"
)

code_block(
"dataset/fault_dataset.csv"
)

P(
    "This file becomes the bridge between the hardware-verification environment "
    "and the Python machine-learning environment."
)

H2("12.3 Why This Bridge Matters")

P(
    "The project is not simply a Python ML project using arbitrary numbers. "
    "The numbers originate from actual RTL simulation behavior."
)

P(
    "Therefore the ML model is trained on hardware-verification evidence."
)

new_page()

# ============================================================
# 13 DATASET
# ============================================================

H1("13. Custom Dataset Generation")

P(
    "One of the strongest parts of this project is the creation of a custom "
    "dataset specifically for RTL fault diagnosis."
)

H2("13.1 Dataset Creation Formula")

P(
    "<b>6 fault classes × 32 behavioral windows × 32 vectors = 6,144 raw observations</b>",
    "Important"
)

H2("13.2 Why 1,024 Rows per Fault?")

P(
    "Each fault is tested over 32 behavioral windows. Each window contains "
    "32 vectors. Therefore:"
)

P(
    "32 × 32 = 1,024 observations per fault."
)

P(
    "With six fault classes:"
)

P(
    "1,024 × 6 = 6,144 total observations."
)

H2("13.3 Balanced Classes")

make_table(
    [
        ["Fault ID", "Observations"],
        ["1", "1,024"],
        ["2", "1,024"],
        ["3", "1,024"],
        ["4", "1,024"],
        ["5", "1,024"],
        ["6", "1,024"],
        ["TOTAL", "6,144"],
    ],
    [6 * cm, 6 * cm]
)

P(
    "The balanced distribution prevents one fault class from dominating the "
    "raw dataset simply because it has more observations."
)

new_page()

# ============================================================
# 14 RAW DATASET
# ============================================================

H1("14. Raw Dataset Structure")

P(
    "The raw dataset contains 11 columns."
)

make_table(
    [
        ["Column", "Description"],
        ["fault_id", "Known injected fault class"],
        ["A", "First 4-bit operand"],
        ["B", "Second 4-bit operand"],
        ["OP", "2-bit operation code"],
        ["expected_result", "Golden result"],
        ["expected_carry", "Golden carry"],
        ["actual_result", "Observed faulty result"],
        ["actual_carry", "Observed faulty carry"],
        ["result_error", "Result mismatch flag"],
        ["carry_error", "Carry mismatch flag"],
        ["bit_errors", "Number of incorrect result bits"],
    ],
    [5 * cm, 11 * cm],
    7.5
)

H2("14.1 Example Row")

make_table(
    [
        [
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
            "bit_errors",
        ],
        ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ],
    [1.25 * cm] * 11,
    6.5
)

P(
    "The first rows can contain no errors because some input combinations "
    "do not activate the injected fault. This is expected and is actually "
    "important for learning the behavioral pattern."
)

H2("14.2 Why Passing Vectors Matter")

P(
    "A faulty design does not necessarily fail every test. The combination of "
    "passing and failing vectors is itself part of the behavioral fingerprint."
)

new_page()

# ============================================================
# 15 DATASET STATISTICS
# ============================================================

H1("15. Dataset Statistics")

P(
    "The final dataset contains:"
)

make_table(
    [
        ["Metric", "Value"],
        ["Rows", "6,144"],
        ["Columns", "11"],
        ["Fault classes", "6"],
        ["Rows per fault", "1,024"],
        ["Operations", "4"],
        ["Rows per operation", "1,536"],
        ["Missing values", "0"],
    ],
    [7 * cm, 9 * cm]
)

H2("15.1 Error Statistics")

make_table(
    [
        ["Fault", "Result Errors", "Carry Errors", "Bit Errors"],
        ["1", "0", "56", "0"],
        ["2", "240", "0", "512"],
        ["3", "256", "0", "1024"],
        ["4", "148", "0", "192"],
        ["5", "240", "0", "512"],
        ["6", "256", "0", "640"],
    ],
    [3 * cm, 4 * cm, 4 * cm, 5 * cm]
)

H2("15.2 Interpretation")

P(
    "Fault #1 is primarily a carry-level fault. Its result error count and "
    "bit-error count are zero in the analyzed dataset, while carry errors occur."
)

P(
    "Fault #3 has the largest bit-error total because XOR-to-XNOR changes the "
    "logic value of the result bits."
)

P(
    "Faults #2 and #6 both affect AND behavior, which helps explain why they "
    "can be more difficult to distinguish using certain features."
)

P(
    "Fault #4 produces fewer errors than several other logic faults because "
    "OR and XOR produce the same output for some input patterns."
)

new_page()

# ============================================================
# 16 BEHAVIORAL WINDOWS
# ============================================================

H1("16. Behavioral Windows")

P(
    "The raw dataset operates at the individual-vector level. However, diagnosis "
    "is more useful when a group of vectors is considered together."
)

H2("16.1 Window Definition")

P(
    "A behavioral window contains 32 vectors."
)

P(
    "Each fault class contains 32 windows."
)

P(
    "Therefore:"
)

P(
    "6 faults × 32 windows = <b>192 behavioral signatures</b>.",
    "Important"
)

H2("16.2 Why Windows?")

P(
    "Consider two different faults that happen to produce the same output for "
    "one particular input. A single vector cannot reliably distinguish them."
)

P(
    "If 32 carefully generated vectors are considered together, the overall "
    "error distribution becomes more informative."
)

H2("16.3 Window-Level Features")

P(
    "The window aggregation calculates statistics such as:"
)

bullet("Total number of result errors")
bullet("Total number of carry errors")
bullet("Total number of bit errors")
bullet("Number of error vectors")
bullet("Overall error rate")
bullet("Average bit errors")
bullet("Maximum bit errors")
bullet("Operation-specific errors")
bullet("Result-bit error counts")
bullet("Expected and actual carry counts")

H2("16.4 Behavioral Fingerprint")

P(
    "The resulting collection of statistics can be viewed as the behavioral "
    "fingerprint of the RTL fault."
)

new_page()

# ============================================================
# 17 SIGNATURES
# ============================================================

H1("17. Behavioral Signatures")

P(
    "The file <b>fault_signatures.csv</b> contains the aggregated behavioral "
    "representation of the raw verification data."
)

P(
    "The dataset contains 192 rows and 49 columns."
)

make_table(
    [
        ["Quantity", "Value"],
        ["Behavioral signatures", "192"],
        ["Total signature columns", "49"],
        ["Excluded columns", "3"],
        ["Final ML features", "46"],
    ],
    [8 * cm, 8 * cm]
)

H2("17.1 Signature Structure")

P(
    "Each signature corresponds to one fault/window combination."
)

P(
    "For example, a signature might represent:"
)

code_block(
"""Fault #1
Window #20
32 verification vectors
        |
        v
Aggregated behavioral statistics
        |
        v
46-dimensional feature vector"""
)

H2("17.2 Signature vs Raw Dataset")

make_table(
    [
        ["Raw Dataset", "Behavioral Signature"],
        ["6,144 rows", "192 rows"],
        ["Individual vectors", "32 vectors aggregated"],
        ["11 columns", "49 columns"],
        ["Detailed observations", "Statistical fingerprint"],
    ],
    [8 * cm, 8 * cm]
)

P(
    "This dimensional abstraction makes the machine-learning problem much "
    "more meaningful for diagnosis."
)

new_page()

# ============================================================
# 18 FEATURE ENGINEERING
# ============================================================

H1("18. Feature Engineering")

P(
    "Feature engineering converts the behavioral signature into numerical "
    "variables that can be supplied to the machine-learning classifier."
)

H2("18.1 Why Feature Engineering?")

P(
    "Machine-learning algorithms work on numerical representations. The raw "
    "RTL verification data contains useful information, but the information "
    "must be structured so that the classifier can recognize patterns."
)

H2("18.2 Excluded Columns")

make_table(
    [
        ["Column", "Reason for exclusion"],
        ["fault_id", "This is the target label."],
        ["window_id", "Identifier, not behavioral evidence."],
        ["num_vectors", "Constant/structural information rather than fault identity."],
    ],
    [5 * cm, 11 * cm]
)

P(
    "Therefore:"
)

P(
    "<b>49 total columns − 3 excluded columns = 46 ML features.</b>",
    "Important"
)

H2("18.3 Feature Categories")

make_table(
    [
        ["Category", "Examples"],
        ["Global errors", "total_result_errors, total_bit_errors"],
        ["Rates", "error_rate"],
        ["Bit statistics", "avg_bit_errors, max_bit_errors"],
        ["Operand statistics", "avg_A, avg_B, A_ones_total"],
        ["ADD behavior", "ADD_result_errors, ADD_carry_errors"],
        ["AND behavior", "AND_result_errors, AND_bit_errors"],
        ["OR behavior", "OR_result_errors, OR_bit_errors"],
        ["XOR behavior", "XOR_result_errors, XOR_bit_errors"],
        ["Result-bit behavior", "s0_error_count ... s3_error_count"],
        ["Carry behavior", "expected_carry_count, actual_carry_count"],
    ],
    [5 * cm, 11 * cm]
)

new_page()

# ============================================================
# 19 46 FEATURES
# ============================================================

H1("19. The 46 ML Features")

features = [
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
    "XOR_bit_errors",
    "XOR_error_rate",
    "XOR_avg_bit_errors",
    "XOR_max_bit_errors",
    "s0_error_count",
    "s1_error_count",
    "s2_error_count",
    "s3_error_count",
    "expected_carry_count",
    "actual_carry_count",
]

feature_rows = [["No.", "Feature"]]

for i, feature in enumerate(features, 1):
    feature_rows.append([str(i), feature])

make_table(
    feature_rows,
    [2 * cm, 14 * cm],
    7.5
)

P(
    "These 46 features form the complete input representation used by the final "
    "Random Forest classifier."
)

new_page()

# ============================================================
# 20 WHY ML
# ============================================================

H1("20. Why Machine Learning?")

P(
    "A deterministic verification environment can tell us that the behavior "
    "is incorrect. However, once multiple possible faults exist, automatically "
    "mapping an observed error pattern to the most likely fault becomes a "
    "classification problem."
)

H2("20.1 Conventional Rule-Based Diagnosis")

P(
    "A simple approach would be to write rules such as:"
)

code_block(
"""IF carry errors occur only during ADD
THEN Fault #1

IF AND operation produces OR-like behavior
THEN Fault #2

IF XOR result is inverted
THEN Fault #3"""
)

P(
    "This can work for a small demonstration, but it becomes difficult to "
    "maintain as the number of faults and behavioral features increases."
)

H2("20.2 ML-Based Diagnosis")

P(
    "Machine learning provides a statistical approach. Instead of manually "
    "writing every rule, the model learns relationships from labeled examples."
)

P(
    "The classifier receives the 46-feature signature and estimates the "
    "probability of each fault class."
)

H2("20.3 Important Principle")

P(
    "<b>AI does not replace verification.</b>",
    "Important"
)

P(
    "The verification environment still generates the evidence. AI interprets "
    "that evidence."
)

new_page()

# ============================================================
# 21 MODEL EXPERIMENTS
# ============================================================

H1("21. Machine Learning Model Experiments")

P(
    "The project experimented with multiple classification algorithms before "
    "selecting the final Random Forest baseline."
)

make_table(
    [
        ["Model", "Initial signature split accuracy"],
        ["Decision Tree", "100.00%"],
        ["Random Forest", "100.00%"],
        ["SVM RBF", "100.00%"],
    ],
    [8 * cm, 8 * cm]
)

P(
    "The 100% result from the initial split should not be interpreted as proof "
    "of perfect real-world generalization because related behavioral windows "
    "can make random train/test splitting optimistic."
)

P(
    "Therefore, the project introduced group-based cross-validation."
)

H2("21.1 Why Group Validation?")

P(
    "The 192 signatures are organized into 32 behavioral windows. Samples from "
    "the same window should not be allowed to leak into both training and testing."
)

P(
    "Group validation keeps complete behavioral windows together."
)

H2("21.2 Models Tested")

bullet("Decision Tree")
bullet("Random Forest")
bullet("SVM with RBF kernel")
bullet("Random Forest variants during hyperparameter tuning")
bullet("Hierarchical global + specialist architecture")

P(
    "After the experiments, the global Random Forest remained the preferred "
    "architecture."
)

new_page()

# ============================================================
# 22 RANDOM FOREST
# ============================================================

H1("22. Random Forest")

P(
    "Random Forest is an ensemble machine-learning algorithm based on multiple "
    "decision trees."
)

H2("22.1 Basic Idea")

P(
    "Instead of relying on a single decision tree, Random Forest trains many "
    "trees using different subsets of the training data and feature space."
)

P(
    "Each tree makes a prediction. The forest combines those predictions to "
    "produce the final class."
)

H2("22.2 Why It Fits This Project")

bullet("The dataset is relatively small.")
bullet("The features are numerical.")
bullet("Behavioral relationships may be nonlinear.")
bullet("Different features interact with each other.")
bullet("Feature importance can be extracted.")
bullet("It does not require the features to be normally distributed.")

H2("22.3 Final Configuration")

make_table(
    [
        ["Parameter", "Final value"],
        ["Algorithm", "Random Forest"],
        ["Trees", "500"],
        ["Input features", "46"],
        ["Classes", "6"],
        ["Training signatures", "192"],
    ],
    [7 * cm, 9 * cm]
)

H2("22.4 Output")

P(
    "The model predicts one of six classes:"
)

code_block(
"""FAULT #1
FAULT #2
FAULT #3
FAULT #4
FAULT #5
FAULT #6"""
)

new_page()

# ============================================================
# 23 TRAINING
# ============================================================

H1("23. Model Training")

P(
    "The final training stage uses the complete set of 192 behavioral signatures."
)

P(
    "The target column is <b>fault_id</b>. The remaining 46 selected columns "
    "are used as model inputs."
)

H2("23.1 Training Process")

numbered(1, "Load fault_signatures.csv.")
numbered(2, "Separate fault_id from the features.")
numbered(3, "Remove window_id and num_vectors.")
numbered(4, "Construct the 46-feature matrix.")
numbered(5, "Create the Random Forest classifier.")
numbered(6, "Train using all 192 signatures.")
numbered(7, "Save the trained model.")
numbered(8, "Save the feature list.")
numbered(9, "Save model metadata.")
numbered(10, "Save feature importance.")

H2("23.2 Generated Model Files")

code_block(
"""outputs/final_model/
|
|-- final_random_forest.pkl
|-- final_feature_list.csv
|-- model_metadata.csv
|-- final_feature_importance.csv"""
)

H2("23.3 Why Save the Feature List?")

P(
    "The feature list guarantees that runtime diagnosis uses the same feature "
    "ordering expected by the trained model."
)

P(
    "A machine-learning model expects its input columns in the same semantic "
    "order used during training."
)

new_page()

# ============================================================
# 24 CROSS VALIDATION
# ============================================================

H1("24. 4-Fold Group Cross-Validation")

P(
    "The project uses four group-based folds to obtain a stronger estimate of "
    "generalization to unseen behavioral windows."
)

make_table(
    [
        ["Fold", "Accuracy"],
        ["Fold 1", "66.67%"],
        ["Fold 2", "100.00%"],
        ["Fold 3", "100.00%"],
        ["Fold 4", "91.67%"],
        ["Mean", "89.58%"],
        ["Standard Deviation", "13.66%"],
    ],
    [7 * cm, 9 * cm]
)

H2("24.1 Interpretation")

P(
    "Fold 1 is the most difficult fold. The model confused Fault #2 with "
    "Fault #6 and Fault #4 with Fault #1."
)

P(
    "Fold 2 was classified perfectly."
)

P(
    "Fold 3 was also classified perfectly after the final feature/model setup."
)

P(
    "Fold 4 contained confusion between Fault #4 and Fault #5."
)

H2("24.2 Why the Accuracy Is Not 100%")

P(
    "The faults do not all produce completely unique behavioral fingerprints. "
    "Some fault classes share operation-level characteristics."
)

P(
    "For example, Fault #2 and Fault #6 both influence AND behavior. "
    "Therefore, their signatures can overlap."
)

P(
    "This is actually an important result because it shows why diagnosis is "
    "non-trivial rather than merely memorizing a unique label."
)

new_page()

# ============================================================
# 25 TUNING
# ============================================================

H1("25. Random Forest Hyperparameter Tuning")

P(
    "Several Random Forest configurations were tested."
)

make_table(
    [
        ["Model", "Mean Accuracy", "Std Dev"],
        ["RF_500_sqrt", "88.54%", "12.97%"],
        ["RF_1000_sqrt", "88.54%", "12.97%"],
        ["RF_500_log2", "88.54%", "12.97%"],
        ["RF_500_all", "89.58%", "13.66%"],
        ["RF_500_balanced", "89.58%", "13.66%"],
        ["RF_1000_balanced", "89.58%", "13.66%"],
    ],
    [6 * cm, 5 * cm, 5 * cm]
)

H2("25.1 Best Tested Model")

P(
    "<b>RF_500_balanced</b> was selected as the best tested configuration "
    "with a mean group-validation accuracy of <b>89.58%</b>."
)

H2("25.2 Important Observation")

P(
    "Increasing the number of trees from 500 to 1,000 did not improve the "
    "measured group-validation accuracy in the tested configurations."
)

P(
    "This demonstrates an important engineering principle: increasing model "
    "complexity does not automatically produce better generalization."
)

new_page()

# ============================================================
# 26 FEATURE IMPORTANCE
# ============================================================

H1("26. Feature Importance")

P(
    "Random Forest provides a feature-importance measure that indicates which "
    "behavioral variables contributed most strongly to the classification."
)

make_table(
    [
        ["Rank", "Feature", "Importance"],
        ["1", "s3_error_count", "0.116268"],
        ["2", "avg_bit_errors", "0.071322"],
        ["3", "total_bit_errors", "0.069553"],
        ["4", "AND_bit_errors", "0.044728"],
        ["5", "AND_max_bit_errors", "0.042742"],
        ["6", "AND_avg_bit_errors", "0.041932"],
        ["7", "max_bit_errors", "0.041759"],
        ["8", "s2_error_count", "0.041626"],
        ["9", "OR_bit_errors", "0.041487"],
        ["10", "OR_avg_bit_errors", "0.041328"],
    ],
    [2 * cm, 9 * cm, 5 * cm]
)

H2("26.1 What Does This Mean?")

P(
    "The model relies heavily on observable error behavior. Bit-level error "
    "counts are particularly informative."
)

P(
    "For example, s3_error_count tells the model how frequently the most "
    "significant result bit differs from the expected behavior."
)

P(
    "The model therefore does not need to inspect the RTL source code during "
    "classification. It uses the behavioral consequences of the fault."
)

H2("26.2 Engineering Interpretation")

P(
    "This is conceptually similar to a fingerprint. Different faults leave "
    "different behavioral fingerprints in the verification results."
)

new_page()

# ============================================================
# 27 MISCLASSIFICATION
# ============================================================

H1("27. Misclassification Analysis")

P(
    "Misclassification analysis was performed to understand exactly where the "
    "Random Forest struggled."
)

H2("27.1 Global Misclassifications")

make_table(
    [
        ["Actual Fault", "Predicted Fault", "Count"],
        ["2", "6", "8"],
        ["4", "1", "8"],
        ["4", "5", "4"],
    ],
    [5 * cm, 6 * cm, 5 * cm]
)

P(
    "There were 20 misclassified samples in the analyzed cross-validation results."
)

H2("27.2 Fault #2 vs Fault #6")

P(
    "The analysis found that the strongest separator between Fault #2 and Fault #6 "
    "was s3_error_count."
)

make_table(
    [
        ["Feature", "Fault #2 mean", "Fault #6 mean"],
        ["s3_error_count", "4.0", "8.0"],
        ["AND_max_bit_errors", "2.9375", "4.0"],
        ["total_bit_errors", "16.0", "20.0"],
        ["avg_bit_errors", "0.500", "0.625"],
    ],
    [7 * cm, 4.5 * cm, 4.5 * cm]
)

P(
    "The signatures are similar in several other dimensions, which explains "
    "why the classifier can confuse these two faults."
)

H2("27.3 Fault #4 vs Fault #5")

P(
    "Fault #4 and Fault #5 can also overlap because both produce OR-related "
    "behavioral failures."
)

P(
    "The strongest separating features include s3_error_count, OR_avg_bit_errors, "
    "total_bit_errors, OR_bit_errors and OR_result_errors."
)

new_page()

# ============================================================
# 28 HIERARCHICAL
# ============================================================

H1("28. Hierarchical Diagnosis Experiment")

P(
    "An advanced idea was also tested: instead of using one global classifier, "
    "a global Random Forest would first identify a likely fault region and "
    "specialist classifiers would then distinguish between known confusing pairs."
)

H2("28.1 Specialist Pairs")

bullet("Fault #2 vs Fault #6")
bullet("Fault #4 vs Fault #1")
bullet("Fault #4 vs Fault #5")

H2("28.2 Result")

make_table(
    [
        ["Fold", "Global RF", "Hierarchical", "Improvement"],
        ["1", "66.67%", "66.67%", "+0.00%"],
        ["2", "100.00%", "100.00%", "+0.00%"],
        ["3", "100.00%", "66.67%", "-33.33%"],
        ["4", "91.67%", "91.67%", "+0.00%"],
        ["Mean", "89.58%", "81.25%", "-8.33%"],
    ],
    [3 * cm, 4 * cm, 4 * cm, 4 * cm]
)

P(
    "The hierarchical approach reduced overall performance."
)

P(
    "Therefore, the project correctly rejected this architecture rather than "
    "keeping it simply because it sounded more advanced."
)

P(
    "<b>Final decision: retain the tuned global Random Forest.</b>",
    "Important"
)

new_page()

# ============================================================
# 29 FINAL MODEL
# ============================================================

H1("29. Final Model")

P(
    "The final training stage uses all 192 behavioral signatures to train the "
    "production/demo Random Forest model."
)

make_table(
    [
        ["Parameter", "Value"],
        ["Training samples", "192"],
        ["Features", "46"],
        ["Fault classes", "6"],
        ["Trees", "500"],
        ["Model type", "Random Forest"],
    ],
    [7 * cm, 9 * cm]
)

H2("29.1 Saved Model")

P(
    "The final model is stored as:"
)

code_block(
"outputs/final_model/final_random_forest.pkl"
)

H2("29.2 Supporting Files")

code_block(
"""final_feature_list.csv
model_metadata.csv
final_feature_importance.csv"""
)

H2("29.3 Why a Saved Model Is Useful")

P(
    "The model can be loaded later without retraining. This is important for "
    "the diagnosis application because the user should not have to train the "
    "model every time the dashboard starts."
)

new_page()

# ============================================================
# 30 REAL TIME
# ============================================================

H1("30. Real-Time Diagnosis Engine")

P(
    "The real-time diagnosis script represents the inference stage of the "
    "project."
)

H2("30.1 Runtime Flow")

code_block(
"""Load trained Random Forest
        |
        v
Load feature list
        |
        v
Load verification dataset
        |
        v
Select behavioral window
        |
        v
Generate 46-feature vector
        |
        v
Model prediction
        |
        v
Probability distribution
        |
        v
Fault diagnosis"""
)

H2("30.2 Example Diagnosis")

P(
    "A demonstration using Fault #1 and a behavioral window produced:"
)

make_table(
    [
        ["Output", "Result"],
        ["Predicted Fault", "FAULT #1"],
        ["Fault Name", "ADD Carry Fault"],
        ["Affected Operation", "ADD"],
        ["Confidence", "100.00%"],
        ["Result Errors", "0"],
        ["Carry Errors", "2"],
        ["Bit Errors", "0"],
    ],
    [7 * cm, 9 * cm]
)

P(
    "The important point is that the diagnosis is based on the behavioral "
    "signature rather than directly passing the fault_id to the classifier."
)

new_page()

# ============================================================
# 31 STREAMLIT
# ============================================================

H1("31. Streamlit Dashboard")

P(
    "The Streamlit application is the user-facing layer of the project."
)

H2("31.1 Why Streamlit?")

P(
    "The ML model itself is a Python object. A command-line script is useful "
    "during development, but an interactive dashboard makes the system easier "
    "to demonstrate."
)

H2("31.2 Dashboard Responsibilities")

bullet("Present project information.")
bullet("Expose behavioral data for inspection.")
bullet("Allow diagnosis interaction.")
bullet("Display predicted fault.")
bullet("Display confidence/probability.")
bullet("Display behavioral error statistics.")
bullet("Present fault-analysis information in a human-readable way.")

H2("31.3 Running the Application")

code_block(
"""python -m streamlit run app.py"""
)

P(
    "The application is then available through the local Streamlit server."
)

P(
    "The dashboard should be understood as the <b>application layer</b> "
    "around the RTL verification and ML pipeline."
)

H2("31.4 What Streamlit Does NOT Do")

P(
    "Streamlit does not simulate the RTL. Vivado/XSim performs the simulation."
)

P(
    "Streamlit does not train the model every time. The trained Random Forest "
    "is loaded from the saved model file."
)

new_page()

# ============================================================
# 32 IOT
# ============================================================

H1("32. IoT Clarification")

P(
    "The completed Project 2 implementation does <b>not</b> contain an IoT subsystem."
)

P(
    "This is important to document correctly rather than artificially adding "
    "an IoT description that does not exist in the implementation."
)

H2("32.1 What Would Count as IoT?")

P(
    "An IoT implementation would normally involve some combination of a "
    "physical or connected device, sensors, communication, telemetry, a network "
    "protocol, cloud/backend processing, or remote monitoring."
)

H2("32.2 What This Project Actually Contains")

make_table(
    [
        ["Component", "Present?"],
        ["RTL hardware design", "Yes"],
        ["SystemVerilog verification", "Yes"],
        ["Vivado/XSim simulation", "Yes"],
        ["Custom dataset generation", "Yes"],
        ["Machine learning", "Yes"],
        ["Fault diagnosis", "Yes"],
        ["Streamlit dashboard", "Yes"],
        ["Physical sensors", "No"],
        ["MQTT/IoT telemetry", "No"],
        ["Cloud IoT platform", "No"],
        ["Microcontroller IoT node", "No"],
    ],
    [9 * cm, 7 * cm]
)

P(
    "Therefore, the correct technical classification is:"
)

P(
    "<b>AI-Assisted RTL Verification and Fault Diagnosis</b>",
    "Important"
)

new_page()

# ============================================================
# 33 END TO END
# ============================================================

H1("33. Complete End-to-End Working")

P(
    "The complete project can now be understood as one continuous chain."
)

H2("Stage 1 — RTL")

P(
    "A 4-bit ALU defines the expected digital behavior."
)

H2("Stage 2 — Fault Injection")

P(
    "Six intentionally faulty versions introduce known implementation bugs."
)

H2("Stage 3 — Verification")

P(
    "SystemVerilog generates inputs and compares actual behavior against the "
    "golden reference."
)

H2("Stage 4 — Simulation")

P(
    "Vivado/XSim executes the verification environment."
)

H2("Stage 5 — Raw Dataset")

P(
    "The testbench records 6,144 observations containing operands, operations, "
    "expected outputs, actual outputs and error information."
)

H2("Stage 6 — Behavioral Signatures")

P(
    "The raw vectors are grouped into 192 behavioral windows."
)

H2("Stage 7 — Feature Engineering")

P(
    "Each behavioral window is converted into 46 ML features."
)

H2("Stage 8 — Machine Learning")

P(
    "Random Forest learns the mapping from behavioral signature to fault class."
)

H2("Stage 9 — Validation")

P(
    "Group cross-validation estimates how well the model generalizes to unseen "
    "behavioral windows."
)

H2("Stage 10 — Diagnosis")

P(
    "A new behavioral signature is passed to the saved model."
)

H2("Stage 11 — Application")

P(
    "Streamlit displays the diagnosis and supporting behavioral information."
)

new_page()

# ============================================================
# 34 RESULTS
# ============================================================

H1("34. Final Results")

make_table(
    [
        ["Metric", "Final Result"],
        ["Fault classes", "6"],
        ["Raw observations", "6,144"],
        ["Rows per fault", "1,024"],
        ["Behavioral windows", "32"],
        ["Behavioral signatures", "192"],
        ["Signature columns", "49"],
        ["ML features", "46"],
        ["Final model", "Random Forest"],
        ["Trees", "500"],
        ["Group CV mean", "89.58%"],
        ["Group CV standard deviation", "13.66%"],
    ],
    [8 * cm, 8 * cm]
)

H2("34.1 Fault-Wise Hierarchical Results")

make_table(
    [
        ["Fault", "Hierarchical accuracy"],
        ["Fault #1", "100.00%"],
        ["Fault #2", "75.00%"],
        ["Fault #3", "100.00%"],
        ["Fault #4", "37.50%"],
        ["Fault #5", "75.00%"],
        ["Fault #6", "100.00%"],
    ],
    [8 * cm, 8 * cm]
)

H2("34.2 Main Result")

P(
    "The final selected architecture is the global Random Forest because the "
    "hierarchical alternative reduced mean accuracy from 89.58% to 81.25%."
)

P(
    "The project therefore demonstrates not only successful model training but "
    "also model selection based on measured validation performance."
)

new_page()

# ============================================================
# 35 LIMITATIONS
# ============================================================

H1("35. Limitations")

P(
    "The project is a controlled proof-of-concept rather than a complete "
    "industrial ASIC verification platform."
)

H2("35.1 Limited Fault Set")

P(
    "Only six fault classes are currently represented."
)

H2("35.2 Small Signature Dataset")

P(
    "There are 192 behavioral signatures. This is sufficient for demonstrating "
    "the methodology but is small compared with industrial ML datasets."
)

H2("35.3 Controlled ALU")

P(
    "The design under test is a 4-bit ALU. Larger RTL blocks could produce "
    "much more complicated behavioral signatures."
)

H2("35.4 Synthetic/Controlled Dataset")

P(
    "The data is generated from intentionally injected faults. Real silicon "
    "failures may exhibit different characteristics."
)

H2("35.5 Generalization")

P(
    "The 89.58% group-validation result should not be interpreted as a universal "
    "accuracy figure for arbitrary RTL bugs."
)

H2("35.6 No IoT Layer")

P(
    "The project does not currently provide hardware telemetry or cloud-based "
    "remote monitoring."
)

new_page()

# ============================================================
# 36 FUTURE
# ============================================================

H1("36. Future Improvements")

H2("36.1 More RTL Blocks")

P(
    "The methodology could be extended from a 4-bit ALU to larger blocks such "
    "as counters, UARTs, FIFOs, bus interfaces, processors or arithmetic units."
)

H2("36.2 More Fault Types")

P(
    "Additional faults could include stuck-at faults, timing-related faults, "
    "incorrect state transitions, reset faults, width mismatches and control "
    "logic errors."
)

H2("36.3 Larger Dataset")

P(
    "Thousands or millions of behavioral signatures could improve statistical "
    "robustness."
)

H2("36.4 Deep Learning")

P(
    "Sequence models or neural networks could potentially operate directly on "
    "longer verification traces instead of manually aggregated features."
)

H2("36.5 Explainable AI")

P(
    "SHAP or similar methods could explain individual fault predictions."
)

H2("36.6 Automated CI/CD Verification")

P(
    "The system could be integrated into a Git-based RTL verification pipeline "
    "where new simulation failures automatically trigger diagnosis."
)

H2("36.7 Real Hardware Integration")

P(
    "A future version could connect FPGA test results to the diagnosis engine."
)

H2("36.8 IoT Extension")

P(
    "If an IoT requirement is desired in a future version, a connected FPGA or "
    "embedded device could stream verification/diagnostic telemetry to a server "
    "or dashboard."
)

new_page()

# ============================================================
# 37 INTERVIEW
# ============================================================

H1("37. Interview Explanation")

H2("37.1 30-Second Explanation")

P(
    "I built an AI-assisted RTL verification system for a 4-bit ALU. "
    "I intentionally injected six different RTL faults and created a "
    "SystemVerilog verification environment in Vivado/XSim. The testbench "
    "generated 6,144 verification observations, which I converted into "
    "192 behavioral signatures with 46 ML features. I trained and validated "
    "Random Forest models to classify the behavioral signatures into six fault "
    "classes. The final model achieved 89.58% mean accuracy under group-based "
    "cross-validation, and I integrated the diagnosis system into a Streamlit "
    "dashboard."
)

H2("37.2 What Did AI Actually Do?")

P(
    "The AI did not generate the RTL and it did not replace the verification "
    "environment. It learned the relationship between behavioral failure "
    "patterns and known RTL fault classes."
)

H2("37.3 How Did You Create the Dataset?")

P(
    "I created it myself from RTL simulation. I had six faulty ALU designs. "
    "The SystemVerilog testbench applied the verification vectors, calculated "
    "expected behavior, captured actual behavior and stored the differences. "
    "This produced 6,144 raw observations."
)

H2("37.4 Why 46 Features?")

P(
    "The behavioral signature dataset had 49 columns. fault_id was the target, "
    "while window_id and num_vectors were excluded from the ML input. "
    "That left 46 behavioral features."
)

H2("37.5 Why Random Forest?")

P(
    "Random Forest performed well on the structured numerical features, "
    "supports nonlinear relationships and provides feature importance. "
    "The tuned global Random Forest was also better than the tested hierarchical "
    "specialist architecture."
)

H2("37.6 What Was the Most Difficult Part?")

P(
    "A major challenge was distinguishing faults that produce similar behavioral "
    "patterns. Fault #2 and Fault #6, for example, both affect AND behavior. "
    "That is why window-level aggregation and group validation were important."
)

new_page()

# ============================================================
# 38 CONCLUSION
# ============================================================

H1("38. Conclusion")

P(
    "This project demonstrates a complete connection between digital hardware "
    "verification and machine learning."
)

P(
    "The project begins with a simple 4-bit ALU. Controlled RTL faults are "
    "introduced to create known failure modes. A SystemVerilog verification "
    "environment running in Vivado/XSim exercises those designs and compares "
    "their outputs against golden behavior."
)

P(
    "Instead of discarding the verification results after determining pass/fail, "
    "the project transforms them into a structured dataset. The final dataset "
    "contains 6,144 raw observations."
)

P(
    "These observations are aggregated into 192 behavioral signatures. "
    "Feature engineering converts each signature into 46 numerical behavioral "
    "features representing global errors, operation-specific behavior, "
    "bit-level errors, carry behavior and other statistics."
)

P(
    "Machine learning is then used to learn the relationship between these "
    "behavioral fingerprints and the six known RTL fault classes."
)

P(
    "Multiple algorithms were evaluated. Group-based validation showed that "
    "the final Random Forest achieved a mean accuracy of 89.58% with a standard "
    "deviation of 13.66%."
)

P(
    "The project also demonstrates an important engineering practice: not every "
    "more complicated model is automatically better. The hierarchical diagnosis "
    "architecture reduced performance and was therefore rejected."
)

P(
    "The final trained Random Forest is integrated into a diagnosis engine and "
    "a Streamlit dashboard, completing the path from RTL simulation to "
    "AI-assisted diagnosis."
)

P(
    "<b>In one sentence:</b>",
    "Important"
)

P(
    "The project converts RTL verification failures into behavioral fingerprints "
    "and uses machine learning to identify the most likely underlying RTL fault.",
    "Important"
)

H2("Final Project Identity")

make_table(
    [
        ["Category", "Final Description"],
        ["Project type", "AI-Assisted RTL Verification"],
        ["Hardware domain", "VLSI / Digital Design"],
        ["Design under test", "4-bit ALU"],
        ["Verification", "SystemVerilog + Vivado/XSim"],
        ["Dataset", "Custom dataset generated from simulation"],
        ["AI/ML", "Random Forest fault classification"],
        ["Application", "Streamlit diagnosis dashboard"],
        ["IoT", "Not included in current implementation"],
    ],
    [6 * cm, 10 * cm]
)

spacer(0.5)

P(
    "<b>END OF REPORT</b>",
    "Center"
)

# ============================================================
# FOOTER
# ============================================================

def add_footer(canvas, doc):
    canvas.saveState()

    canvas.setFont("Helvetica", 7)

    canvas.drawString(
        1.6 * cm,
        0.8 * cm,
        "AI-Assisted RTL Verification & Fault Diagnosis"
    )

    canvas.drawRightString(
        A4[0] - 1.6 * cm,
        0.8 * cm,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# ============================================================
# BUILD PDF
# ============================================================

doc.build(
    story,
    onFirstPage=add_footer,
    onLaterPages=add_footer
)

print("=" * 70)
print("PDF REPORT GENERATED SUCCESSFULLY")
print("=" * 70)
print()
print("File:")
print(OUTPUT_FILE)
print()
print("The report contains a detailed basic-to-advanced explanation")
print("of the complete AI-assisted RTL verification project.")
print("=" * 70)