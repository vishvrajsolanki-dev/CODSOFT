import streamlit as st
import joblib
import numpy as np

model = joblib.load("models/churn_model.pkl")
scaler = joblib.load("models/scaler.pkl")
le_geo = joblib.load("models/le_geo.pkl")
le_gen = joblib.load("models/le_gen.pkl")

st.title("Bank Customer Churn Predictor")
st.markdown("Enter customer details to get churn risk score.")

credit_score = st.slider("Credit Score", 300, 850, 650)
geography = st.selectbox("Geography", le_geo.classes_)
gender = st.selectbox("Gender", le_gen.classes_)
age = st.slider("Age", 18, 92, 35)
tenure = st.slider("Tenure (years)", 0, 10, 5)
balance = st.number_input("Account Balance", min_value=0.0, value=50000.0)
num_products = st.selectbox("Number of Products", [1, 2, 3, 4])
has_cr_card = st.selectbox("Has Credit Card?", ["Yes", "No"])
is_active = st.selectbox("Is Active Member?", ["Yes", "No"])
salary = st.number_input("Estimated Salary", min_value=0.0, value=50000.0)

if st.button("Predict Churn Risk"):
    geo_enc = le_geo.transform([geography])[0]
    gen_enc = le_gen.transform([gender])[0]
    cr_card = 1 if has_cr_card == "Yes" else 0
    active = 1 if is_active == "Yes" else 0

    features = np.array([[credit_score, geo_enc, gen_enc, age, tenure,
                          balance, num_products, cr_card, active, salary]])
    features_scaled = scaler.transform(features)

    prob = model.predict_proba(features_scaled)[0][1]
    label = "High Risk" if prob > 0.5 else "Low Risk"

    st.subheader(f"Churn Probability: {prob:.2%}")
    st.markdown(f"**{label}**")
    st.progress(float(prob))