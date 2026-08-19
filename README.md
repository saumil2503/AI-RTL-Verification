# AI-Assisted RTL Verification & Fault Diagnosis

An end-to-end **VLSI / RTL Verification + Machine Learning** project that combines **SystemVerilog-based fault injection**, **Vivado/XSim behavioral verification**, **behavioral dataset generation**, **feature engineering**, and **machine-learning-based RTL fault diagnosis**.

The project uses a **4-bit ALU** as the target RTL design. Multiple intentional RTL implementation faults are injected into the ALU and exercised using a SystemVerilog verification environment.

The resulting verification behavior is converted into **behavioral signatures containing 46 ML features**, which are used to train a **Random Forest classifier** capable of identifying the most likely underlying RTL fault.

A **Streamlit dashboard** provides an interactive interface for analyzing verification behavior and performing AI-assisted fault diagnosis.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Project Objectives](#project-objectives)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [RTL Design](#rtl-design)
- [Fault Injection](#fault-injection)
- [Verification Environment](#verification-environment)
- [Dataset Generation](#dataset-generation)
- [Dataset Structure](#dataset-structure)
- [Feature Engineering](#feature-engineering)
- [Behavioral Signatures](#behavioral-signatures)
- [Machine Learning](#machine-learning)
- [Model Validation](#model-validation)
- [Feature Importance](#feature-importance)
- [Fault Confusion Analysis](#fault-confusion-analysis)
- [Hierarchical Diagnosis Experiment](#hierarchical-diagnosis-experiment)
- [Final AI Model](#final-ai-model)
- [Real-Time Diagnosis](#real-time-diagnosis)
- [Streamlit Dashboard](#streamlit-dashboard)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Understanding the Workflow](#understanding-the-workflow)
- [Results](#results)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Conclusion](#conclusion)

---

# Project Overview

Traditional RTL verification primarily answers:

> **Does the RTL implementation behave correctly for the given verification vectors?**

This project extends the verification process with a second question:

> **If the RTL fails, can the behavioral failure pattern be used to identify the likely underlying RTL fault automatically?**

The project therefore combines two domains:

### RTL Verification

SystemVerilog and Vivado/XSim are used to:

- create the RTL design
- inject intentional faults
- generate verification vectors
- compare expected and actual behavior
- identify result errors
- identify carry errors
- calculate bit-level errors
- generate behavioral verification data

### Machine Learning

Python and scikit-learn are then used to:

- analyze the verification dataset
- generate behavioral signatures
- extract 46 ML features
- train classification models
- perform group-based cross-validation
- analyze feature importance
- investigate fault confusion
- train the final Random Forest
- diagnose previously unseen behavioral signatures

The overall concept is:

```text
RTL IMPLEMENTATION
        │
        ▼
FAULT INJECTION
        │
        ▼
SYSTEMVERILOG VERIFICATION
        │
        ▼
VIVADO / XSIM
        │
        ▼
RAW VERIFICATION DATA
        │
        ▼
DATASET GENERATION
        │
        ▼
BEHAVIORAL SIGNATURES
        │
        ▼
46 ML FEATURES
        │
        ▼
RANDOM FOREST CLASSIFIER
        │
        ▼
FAULT DIAGNOSIS
        │
        ▼
STREAMLIT DASHBOARD