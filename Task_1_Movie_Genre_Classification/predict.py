import pickle
import os
from utils import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'models', 'model.pkl'), 'rb') as f:
    model = pickle.load(f)
with open(os.path.join(BASE_DIR, 'models', 'vectorizer.pkl'), 'rb') as f:
    vectorizer = pickle.load(f)

def predict_genre(plot_summary):
    cleaned = clean_text(plot_summary)
    vec = vectorizer.transform([cleaned])
    return model.predict(vec)[0]

if __name__ == '__main__':
    sample = "A detective investigates a series of murders in a small coastal town."
    print(f"Predicted genre: {predict_genre(sample)}")