import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
import joblib
import os

print("Loading data...")
train_df = pd.read_csv("data/fraudTrain.csv")
test_df = pd.read_csv("data/fraudTest.csv")

def preprocess(df):
    df = df.copy()

    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['trans_hour'] = df['trans_date_trans_time'].dt.hour
    df['trans_day'] = df['trans_date_trans_time'].dt.dayofweek
    df['trans_month'] = df['trans_date_trans_time'].dt.month

    df['dob'] = pd.to_datetime(df['dob'])
    df['age'] = (df['trans_date_trans_time'] - df['dob']).dt.days // 365

    df['distance'] = np.sqrt(
        (df['lat'] - df['merch_lat'])**2 + (df['long'] - df['merch_long'])**2
    )

    drop_cols = ['Unnamed: 0', 'trans_date_trans_time', 'cc_num',
                 'first', 'last', 'street', 'trans_num', 'dob', 'unix_time']
    df.drop(columns=drop_cols, inplace=True)

    cat_cols = ['merchant', 'category', 'gender', 'city', 'state', 'job']
    le = LabelEncoder()
    for col in cat_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    return df

print("Preprocessing train set...")
train_clean = preprocess(train_df)

print("Preprocessing test set...")
test_clean = preprocess(test_df)

X_train = train_clean.drop(columns=['is_fraud'])
y_train = train_clean['is_fraud']

X_test = test_clean.drop(columns=['is_fraud'])
y_test = test_clean['is_fraud']

print(f"Before SMOTE: {y_train.value_counts().to_dict()}")

print("Applying SMOTE (this will take a few minutes on 1.2M rows)...")
smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)

print(f"After SMOTE: {pd.Series(y_train_bal).value_counts().to_dict()}")

os.makedirs("models", exist_ok=True)
joblib.dump((X_train_bal, y_train_bal, X_test, y_test), "models/processed_data.pkl")

print("Saved to models/processed_data.pkl")