{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "71f73a12-585e-484c-afd8-1bbaaa65e75e",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Movie Genre Classification\n",
    "\n",
    "Predicts the genre of a movie based on its plot summary.\n",
    "Built for the CodSoft Machine Learning Internship.\n",
    "\n",
    "## Dataset\n",
    "IMDB Genre Classification dataset — 54,214 labeled plot summaries,\n",
    "27 genres. Separator: `:::`.\n",
    "\n",
    "## Approach\n",
    "- Text cleaned using NLTK (stopwords removed, Porter stemming)\n",
    "- TF-IDF vectorization with 10,000 features\n",
    "- Three classifiers compared: Naive Bayes, Logistic Regression, LinearSVC\n",
    "\n",
    "## Results\n",
    "| Model | Accuracy |\n",
    "|---|---|\n",
    "| Naive Bayes | 49.96% |\n",
    "| Logistic Regression | 58.38% |\n",
    "| LinearSVC | 56.99% |\n",
    "\n",
    "Logistic Regression performed best on this dataset.\n",
    "\n",
    "## Files\n",
    "- `Task_1_Movie_Genre_Classification.ipynb` — main notebook\n",
    "- `genre_distribution.png` — class distribution\n",
    "- `model_comparison.png` — accuracy comparison\n",
    "- `confusion_matrix.png` — per-genre prediction breakdown\n",
    "- `wordclouds.png` — dominant words per genre\n",
    "\n",
    "## Libraries\n",
    "pandas, numpy, nltk, scikit-learn, matplotlib, seaborn, wordcloud\n",
    "\n",
    "## Author\n",
    "Vishvrajsinh Solanki — CodSoft ML Intern"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
