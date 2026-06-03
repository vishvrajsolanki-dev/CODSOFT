# Credit Card Fraud Detection

A machine learning project that detects fraudulent credit card transactions using XGBoost and SMOTE-based class balancing.

## Problem

Fraud transactions make up less than 1% of all transactions. A naive model that predicts everything as legitimate achieves 99% accuracy but is completely useless. This project addresses that imbalance directly.

## Dataset

Transaction dataset split into train (1.29M rows) and test (555K rows) sets.
Fraud rate: 0.58%

## Approach

- Extracted time-based features from transaction timestamps (hour, day, month)
- Computed cardholder age from date of birth
- Computed geographic distance between cardholder and merchant
- Applied SMOTE to balance the training set from 0.58% fraud to 50/50
- Trained an XGBoost classifier on the balanced data
- Evaluated using Precision, Recall, F1-score, and ROC-AUC

## Results

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.9771 |
| Fraud Recall | 88% |
| Overall Accuracy | 98% |

Recall was prioritized over precision. Missing a fraud is worse than a false alarm.

## Tech Stack

- Python 3.11
- pandas, numpy
- scikit-learn
- imbalanced-learn (SMOTE)
- XGBoost
- matplotlib, seaborn
- Streamlit

## Project Structure

credit-fraud-detection/
├── data/
├── models/
├── preprocess.py
├── train.py
├── evaluate.py
├── app.py
└── requirements.txt

## Usage

python preprocess.py
python train.py
python evaluate.py
streamlit run app.py

## Author

Vishvraj