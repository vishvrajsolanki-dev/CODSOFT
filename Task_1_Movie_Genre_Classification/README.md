# PlotSense (CineGenius) — Movie Genre Classification

Predicts a movie's genre from its plot summary using TF-IDF + Logistic Regression, wrapped in a Streamlit app.

## What It Does

Takes a plot summary as input and classifies it across **27 genres**, trained on **54,214 samples**.

## Approach

- **Vectorization:** TF-IDF, `max_features=10,000`, `ngram_range=(1,2)`
- **Model:** Logistic Regression, `C=5`
- **Result:** 58.38% accuracy across 27 classes — a meaningfully hard multi-class problem (plot summaries are short, genres overlap, and 27-way classification has a much lower random baseline than binary tasks)

## Stack

Python · scikit-learn · TF-IDF · Logistic Regression · Streamlit

## UI

Streamlit app with a cinematic dark-gold theme.

---

*CodSoft Machine Learning Internship — Task 1*
