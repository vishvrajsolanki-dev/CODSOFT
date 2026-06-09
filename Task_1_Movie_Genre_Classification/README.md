# Movie Genre Classification

Predicts the genre of a movie based on its plot summary.
Built for the CodSoft Machine Learning Internship.

## Dataset
IMDB Genre Classification dataset - 54,214 labeled plot summaries, 27 genres. Separator: `:::`.

## Approach
- Text cleaned using NLTK (stopwords removed, Porter stemming)
- TF-IDF vectorization with 10,000 features
- Three classifiers compared: Naive Bayes, Logistic Regression, LinearSVC

## Results
| Model | Accuracy |
|---|---|
| Naive Bayes | 49.96% |
| Logistic Regression | 58.38% |
| LinearSVC | 56.99% |

Logistic Regression performed best on this dataset.

## Files
- Task_1_Movie_Genre_Classification.ipynb
- genre_distribution.png, model_comparison.png, confusion_matrix.png, wordclouds.png

## Libraries
pandas, numpy, nltk, scikit-learn, matplotlib, seaborn, wordcloud

## Author
Vishvrajsinh Solanki - CodSoft ML Intern