from sklearn.ensemble import GradientBoostingClassifier
import joblib

X_train = joblib.load("models/X_train.pkl")
y_train = joblib.load("models/y_train.pkl")

model = GradientBoostingClassifier(n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "models/churn_model.pkl")
print("Model trained and saved.")