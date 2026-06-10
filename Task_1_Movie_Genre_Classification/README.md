# Task 1 — Movie Genre Classification

Predicts the genre of a movie based on its plot summary using classical NLP and machine learning.

## Live Demo
> Add your Streamlit Cloud URL here after deployment

## Task
Build a machine learning model that classifies movies into genres based on plot summaries using TF-IDF vectorization and text classifiers.

## Dataset
IMDB Genre Classification Dataset — 54,214 labeled plot summaries across 27 genres.
Separator: `:::` | Format: `ID ::: TITLE ::: GENRE ::: DESCRIPTION`

## Approach
- Text preprocessing with NLTK (stopword removal, Porter stemming)
- TF-IDF vectorization (50,000 features, bigrams, sublinear TF scaling)
- Three classifiers benchmarked: Naive Bayes, Logistic Regression, LinearSVC
- Logistic Regression selected as best performer

## Results

| Model | Accuracy |
|---|---|
| Naive Bayes | 49.96% |
| Logistic Regression | **60.25%** |
| LinearSVC | 56.99% |

## Project Structure

    Task_1_Movie_Genre_Classification/
    ├── app.py            # Streamlit web application
    ├── train.py          # Model training script
    ├── predict.py        # Prediction logic
    ├── utils.py          # Text cleaning utilities
    ├── models/           # Saved model and vectorizer (.pkl)
    ├── data/             # Dataset files
    └── requirements.txt

## Setup and Usage

**1. Install dependencies**

    pip install -r requirements.txt

**2. Train the model**

    python train.py

**3. Run the app**

    streamlit run app.py

## Libraries

pandas, numpy, nltk, scikit-learn, streamlit

## Author

**Vishvrajsinh Solanki** — CodSoft ML Internship