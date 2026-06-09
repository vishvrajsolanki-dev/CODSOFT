import joblib
import time
from xgboost import XGBClassifier

print("Loading processed data...")
X_train, y_train, X_test, y_test = joblib.load("models/processed_data.pkl")

print(f"Training samples: {X_train.shape[0]:,}")
print(f"Features: {X_train.shape[1]}")

model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42,
    n_jobs=-1
)

print("Training model...")
start = time.time()
model.fit(X_train, y_train)
elapsed = time.time() - start

print(f"Training done in {elapsed:.1f} seconds")

joblib.dump((model, X_test, y_test), "models/fraud_model.pkl")
print("Model saved to models/fraud_model.pkl")