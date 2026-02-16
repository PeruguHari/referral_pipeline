# Referral Data Pipeline & Fraud Validation

## 📌 Objective

This project implements a data profiling and referral validation pipeline using **Python (Pandas)**.  
The pipeline models a user referral program and applies business rules to identify valid and invalid referral rewards, helping detect potential fraud scenarios.

---

## 🧩 Project Components

✔ Data Profiling  
✔ Data Cleaning  
✔ Data Transformation  
✔ Timezone Adjustment  
✔ Table Joins  
✔ Business Logic Validation  
✔ Fraud Detection Flag  
✔ Docker Containerization  

---

## 📂 Project Structure

- referral_pipeline/
  - Dockerfile
  - requirements.txt
  - README.md
  - profiling_report.csv
  - data/
    - lead_log.csv
    - paid_transactions.csv
    - referral_rewards.csv
    - user_logs.csv
    - user_referral_logs.csv
    - user_referral_statuses.csv
    - user_referrals.csv
  - src/
    - pipeline.py
    - profiling.py
  - output/
    - referral_validation_report.csv


---

## 📊 Data Profiling

The profiling script calculates:

- Null value counts
- Distinct value counts
- Data types

## ▶ Run Profiling (without Docker)
- cd src
- python profiling.py


---

## 📊 Output
- profiling_report.csv

---

## ⚙️ Pipeline Execution

The pipeline performs:

✔ Timestamp conversion to datetime  
✔ Reward value normalization ("30 days" → 30)  
✔ Removal of invalid/null keys  
✔ String formatting (Initcap)  
✔ Joining related tables  
✔ Applying business validation rules  

---

### ▶ Run Pipeline (without Docker)
cd src
python pipeline.py


## 📊 Output
- output/referral_validation_report.csv

---
## 🐳 Docker Support
This application is containerized to ensure reproducibility.

## ▶ Build Docker Image
Run from project root:

 - docker build -t referral_pipeline .

## ▶ Run Docker Container
 - PowerShell
    - docker run --rm -v ${PWD}/output:/app/output referral_pipeline
  - Command Prompt (CMD)
    - docker run --rm -v %cd%/output:/app/output referral_pipeline

## 📈 Output Report

The final output contains:

 ✔ Referral details  
 ✔ Referrer details  
✔ Referee details  
✔ Reward information  
✔ Transaction verification  
✔ Business logic validity flag  


---
