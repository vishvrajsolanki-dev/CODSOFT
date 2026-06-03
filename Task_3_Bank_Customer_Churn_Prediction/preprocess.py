import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

os.makedirs("models", exist_ok=True)

df = pd.read_csv("data/Churn_Modelling.csv")
df.drop(columns=["RowNumber", "CustomerId", "Surname"], inplace=True)

le_geo = LabelEncoder()
le_gen = LabelEncoder()
df["Geography"] = le_geo.fit_transform(df["Geography"])
df["Gender"] = le_gen.fit_transform(df["Gender"])

X = df.drop(columns=["Exited"])
y = df["Exited"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

joblib.dump(X_train, "models/X_train.pkl")
joblib.dump(X_test, "models/X_test.pkl")
joblib.dump(y_train, "models/y_train.pkl")
joblib.dump(y_test, "models/y_test.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(le_geo, "models/le_geo.pkl")
joblib.dump(le_gen, "models/le_gen.pkl")

print("Preprocessing done. models/ populated.")