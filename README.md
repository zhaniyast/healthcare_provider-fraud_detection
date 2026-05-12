# Real-Time Healthcare Fraud Detection System 

## Project Overview
This project implements a machine learning pipeline to detect fraudulent healthcare providers using Medicare claims data. By analyzing patterns in inpatient, outpatient, and beneficiary records, the system identifies anomalous billing behaviors with high precision.

The repository includes a full end-to-end workflow: from data cleaning and feature engineering to model deployment readiness.

## Real-Time Architecture
Unlike traditional batch processing, this project is designed for **Real-Time Inference**. 
- **Model Serialization:** The trained model is exported as a `.pkl` file.
- **Threshold Optimization:** Logic is included to determine the optimal decision boundary for immediate "Fraud/No-Fraud" flagging.
- **Feature Mapping:** Feature columns are mapped to JSON to ensure the production environment mirrors the training environment exactly.

## Dataset
The analysis uses the **Healthcare Provider Fraud Detection Analysis** dataset, which includes:
* **Inpatient/Outpatient Claims:** Visit details, procedure codes, and reimbursement amounts.
* **Beneficiary Records:** Patient demographics and chronic condition history.
* **Ground Truth:** Labels identifying providers previously flagged for fraudulent activity.

## Tech Stack
* **Language:** Python
* **Libraries:** Pandas, NumPy, Scikit-Learn, XGBoost, Matplotlib, Seaborn
* **Deployment Tools:** Joblib (for model persistence), JSON (for metadata)

## Methodology & Results
1. **Data Aggregation:** Transformed claim-level data into provider-level features (e.g., average reimbursement per provider, number of unique physicians).
2. **Handling Imbalance:** Addressed the highly imbalanced nature of fraud data using specialized sampling and threshold tuning.
3. **Modeling:**
   - **XGBoost:** Achieved the highest predictive power for complex patterns.
   - **Logistic Regression:** Used for baseline performance and interpretability.
4. **Evaluation:** Focused on **Recall** and **AUC-ROC** to ensure maximum detection of fraudulent actors.

## Team Members

This project was developed as a group assignment for the **Regression Analysis** course.

| Name | ID | Primary Contribution |
| :--- | :--- | :--- |
| **Zhaniya Stamshalova** | 230183073 | Data Cleaning & Preprocessing |
| **Orynbassar Nurila** | 230183137 | Lead Modeling & Threshold Optimization |
| **Kosbay Assylzhan** | 230183066 | Streamlit Application Building |
| **Duman Madina** | 230183070 | Feature Engineering & Visualization |
| **Bolatkazy Togzhan** | 230183084 | Documentation & Exploratory Data Analysis (EDA) |

---
*Developed at Suleyman Demirel University (SDU).*
