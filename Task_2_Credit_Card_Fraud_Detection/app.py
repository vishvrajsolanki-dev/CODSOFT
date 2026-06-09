import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

model, X_test, y_test = joblib.load("models/fraud_model.pkl")

st.title("Credit Card Fraud Detection")
st.write("Enter transaction details to check if it is fraudulent.")

amt = st.number_input("Transaction Amount (USD)", min_value=0.01, value=100.0)
category = st.selectbox("Merchant Category", [
    "grocery_pos", "entertainment", "food_dining", "gas_transport",
    "health_fitness", "home", "kids_pets", "misc_net", "misc_pos",
    "personal_care", "shopping_net", "shopping_pos", "travel"
])
gender = st.selectbox("Gender", ["M", "F"])
city_pop = st.number_input("City Population", min_value=100, value=50000)
age = st.slider("Cardholder Age", 18, 90, 35)
trans_hour = st.slider("Transaction Hour (0-23)", 0, 23, 12)
trans_day = st.selectbox("Day of Week", [0, 1, 2, 3, 4, 5, 6],
                         format_func=lambda x: ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][x])
trans_month = st.slider("Month", 1, 12, 6)
distance = st.number_input("Distance from Home (degrees)", min_value=0.0, value=1.5)

lat = st.number_input("Cardholder Latitude", value=37.77)
long = st.number_input("Cardholder Longitude", value=-122.41)
merch_lat = st.number_input("Merchant Latitude", value=38.10)
merch_long = st.number_input("Merchant Longitude", value=-121.90)
zip_code = st.number_input("ZIP Code", value=94103)

le = LabelEncoder()

category_encoded = le.fit_transform([category])[0]
gender_encoded = 0 if gender == "F" else 1

input_data = pd.DataFrame([[
    0,
    category_encoded,
    amt,
    gender_encoded,
    0,
    0,
    zip_code,
    lat,
    long,
    city_pop,
    0,
    trans_hour,
    trans_day,
    trans_month,
    age,
    distance,
    merch_lat,
    merch_long
]], columns=X_test.columns)

if st.button("Check Transaction"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.error(f"Fraud Detected — Confidence: {probability:.2%}")
    else:
        st.success(f"Legitimate Transaction — Fraud Probability: {probability:.2%}")