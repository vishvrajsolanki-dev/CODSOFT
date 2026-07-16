# CODSOFT Machine Learning Internship

Three ML tasks completed as part of the CodSoft ML Internship (May–June 2026). Each subfolder is a standalone project following the same 4-script pipeline pattern: preprocess → train → evaluate → Streamlit app.

| Task | Project | Domain | Headline Metric | Status |
|---|---|---|---|---|
| 1 | [Movie Genre Classification (PlotSense)](./Task_1_Movie_Genre_Classification) | NLP / Text Classification | 60.25% accuracy, 27 genre classes | Live |
| 2 | [Credit Card Fraud Detection](./Task_2_Credit_Card_Fraud_Detection) | Fintech / Fraud Detection | ROC-AUC 0.9771, 88% fraud recall | Local |
| 3 | [Bank Customer Churn Prediction](./Task_3_Bank_Customer_Churn_Prediction) | Fintech / Classification | ROC-AUC 0.8702 | Local |

---

## Task 1 — PlotSense (Movie Genre Classification)
Predicts a movie's genre from a plain-text plot summary. TF-IDF (50k features, bigrams) + Logistic Regression on 54,214 IMDB plot summaries across 27 genre classes. Rebuilt from a raw notebook into a structured, deployed app with a custom cinema-themed UI.

**Live demo:** https://codsoft-hgjtjwr3a4okoiqyowd8ut.streamlit.app/

## Task 2 — Credit Card Fraud Detection
Classifies transactions as fraudulent or legitimate on a highly imbalanced dataset (0.58% fraud rate, 1.29M rows). SMOTE-balanced training set (2.58M samples post-oversampling) + XGBoost. Optimized for recall over raw accuracy — a domain-informed tradeoff for fraud detection.

**Live demo:** https://codsoft-azmp4trfytbh8npieeebut.streamlit.app/

## Task 3 — Bank Customer Churn Prediction
Predicts customer churn likelihood from profile data (10,000 rows). GradientBoostingClassifier with a modular preprocess/train/evaluate/app pipeline and a live risk-scoring Streamlit UI.

**Live demo:** https://codsoft-4deobyqqugvbutwms8izqh.streamlit.app/
---

## Common Stack
Python 3.11, scikit-learn, XGBoost, imbalanced-learn (SMOTE), pandas, NumPy, matplotlib, seaborn, joblib, Streamlit — each task follows the same modular pipeline: `preprocess.py` → `train.py` → `evaluate.py` → `app.py`.
