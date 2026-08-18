# AI-Assisted RTL Verification & Fault Diagnosis

An end-to-end VLSI/RTL verification project that combines **SystemVerilog-based fault injection and verification** with **machine-learning-based behavioral fault diagnosis**.

The system intentionally injects multiple RTL implementation faults into a 4-bit ALU, generates verification data using Vivado/XSim, converts the raw verification results into behavioral signatures, extracts 46 ML features, and trains a Random Forest classifier to identify the most likely RTL fault.

A Streamlit dashboard provides an interactive interface for behavioral-window diagnosis and fault analysis.

---

## Project Overview

Traditional RTL verification determines whether a design passes or fails a set of test vectors. This project extends that concept by asking a second question:

> **Can the behavioral failure pattern be used to automatically identify the underlying RTL fault?**

The project implements the following pipeline:

```text
                    RTL DESIGN
                        │
                        ▼
                FAULT INJECTION
                        │
                        ▼
              SYSTEMVERILOG TB
                        │
                        ▼
                  VIVADO / XSIM
                        │
                        ▼
             VERIFICATION VECTORS
                        │
                        ▼
              BEHAVIORAL DATASET
                        │
                        ▼
             FEATURE ENGINEERING
                        │
                        ▼
             BEHAVIORAL SIGNATURES
                        │
                        ▼
              RANDOM FOREST MODEL
                        │
                        ▼
                FAULT DIAGNOSIS
                        │
                        ▼
             STREAMLIT DASHBOARD