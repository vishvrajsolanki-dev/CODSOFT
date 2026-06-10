import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from utils import clean_text

print("Loading dataset...")
df = pd.read_csv(
    'data/train_data.txt',
    sep=':::',
    engine='python',
    names=['id', 'title', 'genre', 'plot']
)
print(f"Dataset loaded: {len(df)} rows")

print("Cleaning text...")
df['clean_plot'] = df['plot'].apply(clean_text)

X_train, X_test, y_train, y_test = train_test_split(
    df['clean_plot'], df['genre'], test_size=0.2, random_state=42
)

print("Vectorizing text...")
vectorizer = TfidfVectorizer(
    max_features=50000,
    ngram_range=(1, 2),
    sublinear_tf=True,
    min_df=2
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Training model...")
model = LogisticRegression(
    max_iter=1000,
    C=5,
    solver='lbfgs'
)
model.fit(X_train_vec, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test_vec))
print(f"\nAccuracy: {accuracy:.4f}")
print("\nPer-genre breakdown:")
print(classification_report(y_test, model.predict(X_test_vec), zero_division=0))

os.makedirs('models', exist_ok=True)
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("\nModel and vectorizer saved to models/")