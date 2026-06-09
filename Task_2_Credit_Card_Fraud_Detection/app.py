import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FraudGuard — Transaction Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F7F6F3 !important;
    font-family: 'Inter', sans-serif !important;
    color: #0A0A0A !important;
}

[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }

/* ── Main container ── */
.main-wrap {
    max-width: 1100px;
    margin: 0 auto;
    padding: 48px 32px 80px;
}

/* ── Topbar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 48px;
    padding-bottom: 24px;
    border-bottom: 1px solid #E0DDD6;
}
.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}
.brand-icon {
    width: 36px; height: 36px;
    background: #0A0A0A;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.brand-name {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #0A0A0A;
}
.brand-tag {
    font-size: 11px;
    font-weight: 500;
    color: #C8922A;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: #FDF4E4;
    padding: 3px 8px;
    border-radius: 4px;
}

/* ── Page title ── */
.page-title {
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #0A0A0A;
    margin-bottom: 6px;
    line-height: 1.15;
}
.page-sub {
    font-size: 15px;
    color: #6B6860;
    font-weight: 400;
    margin-bottom: 40px;
}

/* ── Section label ── */
.sec-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #C8922A;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid #EAE8E2;
}

/* ── Form card ── */
.form-card {
    background: #FFFFFF;
    border: 1px solid #E5E2DA;
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

/* ── Streamlit widget overrides ── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: #FAFAF8 !important;
    border: 1.5px solid #E0DDD6 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    color: #0A0A0A !important;
    transition: border-color 0.15s;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #C8922A !important;
    box-shadow: 0 0 0 3px rgba(200,146,42,0.12) !important;
    outline: none !important;
}

/* Labels */
label, [data-testid="stWidgetLabel"] p {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #3D3A34 !important;
    letter-spacing: 0.01em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

/* Slider */
[data-testid="stSlider"] > div > div > div {
    background: #C8922A !important;
}

/* Button */
[data-testid="stButton"] > button {
    background: #0A0A0A !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    padding: 14px 32px !important;
    border-radius: 12px !important;
    border: none !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.1s !important;
    margin-top: 8px !important;
}
[data-testid="stButton"] > button:hover {
    background: #2A2A2A !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Result panel ── */
.result-panel {
    background: #FFFFFF;
    border: 1px solid #E5E2DA;
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    position: sticky;
    top: 24px;
}
.result-idle {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 340px;
    gap: 12px;
    text-align: center;
}
.result-idle-icon {
    width: 64px; height: 64px;
    background: #F2EFE9;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
}
.result-idle-text {
    font-size: 14px;
    color: #9B9790;
    font-weight: 500;
    max-width: 200px;
    line-height: 1.5;
}

/* Gauge SVG wrapper */
.gauge-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}
.verdict-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 50px;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: -0.01em;
}
.verdict-fraud {
    background: #FFF0F0;
    color: #C0392B;
    border: 1.5px solid #FADADD;
}
.verdict-legit {
    background: #F0FAF3;
    color: #1E8449;
    border: 1.5px solid #D5F0DD;
}
.prob-label {
    font-size: 12px;
    font-weight: 600;
    color: #9B9790;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}
.prob-value {
    font-size: 48px;
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1;
}
.prob-fraud { color: #C0392B; }
.prob-legit { color: #1E8449; }

.meta-row {
    display: flex;
    justify-content: space-between;
    width: 100%;
    padding: 12px 0;
    border-top: 1px solid #F0EDE7;
    font-size: 13px;
}
.meta-key { color: #9B9790; font-weight: 500; }
.meta-val { color: #0A0A0A; font-weight: 600; }

/* Divider */
.divider { height: 1px; background: #EAE8E2; margin: 24px 0; }

/* Stat pills */
.stat-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 32px;
}
.stat-pill {
    background: #FFFFFF;
    border: 1px solid #E5E2DA;
    border-radius: 10px;
    padding: 12px 20px;
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
    min-width: 120px;
}
.stat-pill-val {
    font-size: 20px;
    font-weight: 700;
    color: #0A0A0A;
    letter-spacing: -0.03em;
}
.stat-pill-label {
    font-size: 11px;
    font-weight: 500;
    color: #9B9790;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.accent { color: #C8922A; }

/* hide default streamlit column gaps on mobile */
[data-testid="stHorizontalBlock"] { gap: 24px !important; }
</style>
""", unsafe_allow_html=True)


# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("models/fraud_model.pkl")

model, X_test, y_test = load_model()


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-wrap">
  <div class="topbar">
    <div class="brand">
      <div class="brand-icon">🛡️</div>
      <span class="brand-name">FraudGuard</span>
    </div>
    <span class="brand-tag">XGBoost · ROC-AUC 0.9771</span>
  </div>

  <div class="page-title">Transaction Risk<br>Intelligence</div>
  <div class="page-sub">Trained on 2.5M transactions · 88% fraud recall · Real-time classification</div>

  <div class="stat-row">
    <div class="stat-pill">
      <span class="stat-pill-val accent">0.9771</span>
      <span class="stat-pill-label">ROC-AUC Score</span>
    </div>
    <div class="stat-pill">
      <span class="stat-pill-val">88%</span>
      <span class="stat-pill-label">Fraud Recall</span>
    </div>
    <div class="stat-pill">
      <span class="stat-pill-val">2.5M</span>
      <span class="stat-pill-label">Training Rows</span>
    </div>
    <div class="stat-pill">
      <span class="stat-pill-val">SMOTE</span>
      <span class="stat-pill-label">Class Balancing</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Layout ────────────────────────────────────────────────────────────────────
col_form, col_result = st.columns([1.1, 0.9], gap="large")

with col_form:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    # ── Section 1: Transaction ──
    st.markdown('<div class="sec-label">Transaction Details</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        amt = st.number_input("Amount (USD)", min_value=0.01, value=100.0, step=0.01)
    with c2:
        category = st.selectbox("Merchant Category", [
            "grocery_pos", "entertainment", "food_dining", "gas_transport",
            "health_fitness", "home", "kids_pets", "misc_net", "misc_pos",
            "personal_care", "shopping_net", "shopping_pos", "travel"
        ])

    c3, c4, c5 = st.columns(3)
    with c3:
        trans_hour = st.slider("Hour of Day", 0, 23, 12)
    with c4:
        trans_day = st.selectbox("Day of Week", [0,1,2,3,4,5,6],
                                  format_func=lambda x: ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"][x])
    with c5:
        trans_month = st.slider("Month", 1, 12, 6)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Section 2: Cardholder ──
    st.markdown('<div class="sec-label">Cardholder Profile</div>', unsafe_allow_html=True)

    c6, c7, c8 = st.columns(3)
    with c6:
        gender = st.selectbox("Gender", ["Male", "Female"])
    with c7:
        age = st.slider("Age", 18, 90, 35)
    with c8:
        city_pop = st.number_input("City Population", min_value=100, value=50000)

    c9, c10 = st.columns(2)
    with c9:
        lat = st.number_input("Cardholder Latitude", value=37.77, format="%.4f")
    with c10:
        long_ = st.number_input("Cardholder Longitude", value=-122.41, format="%.4f")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Section 3: Merchant ──
    st.markdown('<div class="sec-label">Merchant & Location</div>', unsafe_allow_html=True)

    c11, c12 = st.columns(2)
    with c11:
        merch_lat = st.number_input("Merchant Latitude", value=38.10, format="%.4f")
    with c12:
        merch_long = st.number_input("Merchant Longitude", value=-121.90, format="%.4f")

    c13, c14 = st.columns(2)
    with c13:
        zip_code = st.number_input("ZIP Code", value=94103)
    with c14:
        distance = st.number_input("Distance from Home (°)", min_value=0.0, value=1.5, format="%.2f")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    run = st.button("Analyse Transaction →")
    st.markdown('</div>', unsafe_allow_html=True)


# ── Result panel ──────────────────────────────────────────────────────────────
with col_result:
    st.markdown('<div class="result-panel">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Risk Assessment</div>', unsafe_allow_html=True)

    if not run:
        st.markdown("""
        <div class="result-idle">
          <div class="result-idle-icon">🔍</div>
          <div class="result-idle-text">Fill in the transaction details and click Analyse to see the risk score</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Build input
        le = LabelEncoder()
        category_encoded = le.fit_transform([category])[0]
        gender_encoded = 0 if gender == "Female" else 1

        input_data = pd.DataFrame([[
            0, category_encoded, amt, gender_encoded, 0, 0,
            int(zip_code), lat, long_, int(city_pop), 0,
            trans_hour, trans_day, trans_month, age,
            distance, merch_lat, merch_long
        ]], columns=X_test.columns)

        prediction = model.predict(input_data)[0]
        probability = float(model.predict_proba(input_data)[0][1])
        pct = probability * 100

        # Gauge SVG
        # Arc from -140° to +140° (280° sweep)
        # Needle angle maps 0→-140°, 1→+140°
        import math
        sweep = 280
        start_deg = -140
        needle_deg = start_deg + pct / 100 * sweep

        def polar(cx, cy, r, deg):
            rad = math.radians(deg)
            return cx + r * math.cos(rad), cy + r * math.sin(rad)

        cx, cy, R = 140, 120, 100
        track_start = polar(cx, cy, R, start_deg)
        track_end   = polar(cx, cy, R, start_deg + sweep)
        fill_end    = polar(cx, cy, R, needle_deg)

        large_arc  = 1  # always large for track (280°)
        fill_large = 1 if pct >= 50 else 0

        track_d = (f"M {track_start[0]:.1f} {track_start[1]:.1f} "
                   f"A {R} {R} 0 {large_arc} 1 {track_end[0]:.1f} {track_end[1]:.1f}")

        # fill arc — from start to needle
        fill_sweep = pct / 100 * sweep
        fill_large_flag = 1 if fill_sweep > 180 else 0
        fill_d = (f"M {track_start[0]:.1f} {track_start[1]:.1f} "
                  f"A {R} {R} 0 {fill_large_flag} 1 {fill_end[0]:.1f} {fill_end[1]:.1f}")

        # needle line
        n_outer = polar(cx, cy, 82, needle_deg)
        n_inner = polar(cx, cy, 20, needle_deg)

        fill_color = "#C0392B" if prediction == 1 else "#1E8449"
        verdict_cls = "verdict-fraud" if prediction == 1 else "verdict-legit"
        verdict_icon = "⚠️" if prediction == 1 else "✅"
        verdict_text = "Fraud Detected" if prediction == 1 else "Legitimate"
        prob_cls = "prob-fraud" if prediction == 1 else "prob-legit"

        risk_label = "CRITICAL" if pct > 70 else "ELEVATED" if pct > 40 else "LOW"

        gauge_svg = f"""
        <svg viewBox="0 0 280 160" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:280px">
          <!-- track -->
          <path d="{track_d}" fill="none" stroke="#EAE8E2" stroke-width="14" stroke-linecap="round"/>
          <!-- fill -->
          <path d="{fill_d}" fill="none" stroke="{fill_color}" stroke-width="14" stroke-linecap="round" opacity="0.85"/>
          <!-- needle -->
          <line x1="{n_inner[0]:.1f}" y1="{n_inner[1]:.1f}" x2="{n_outer[0]:.1f}" y2="{n_outer[1]:.1f}"
                stroke="#0A0A0A" stroke-width="2.5" stroke-linecap="round"/>
          <!-- hub -->
          <circle cx="{cx}" cy="{cy}" r="7" fill="#0A0A0A"/>
          <circle cx="{cx}" cy="{cy}" r="3" fill="#F7F6F3"/>
          <!-- labels -->
          <text x="40" y="145" font-family="Inter,sans-serif" font-size="9" fill="#9B9790" font-weight="600">LOW RISK</text>
          <text x="200" y="145" font-family="Inter,sans-serif" font-size="9" fill="#9B9790" font-weight="600" text-anchor="end">HIGH RISK</text>
        </svg>
        """

        st.markdown(f"""
        <div class="gauge-wrap">
          {gauge_svg}
          <div class="prob-label">Fraud Probability</div>
          <div class="prob-value {prob_cls}">{pct:.1f}%</div>
          <div class="{verdict_cls} verdict-badge">{verdict_icon} {verdict_text}</div>
        </div>
        <div class="divider" style="margin-top:24px"></div>
        <div class="meta-row">
          <span class="meta-key">Risk Level</span>
          <span class="meta-val">{risk_label}</span>
        </div>
        <div class="meta-row">
          <span class="meta-key">Amount</span>
          <span class="meta-val">${amt:,.2f}</span>
        </div>
        <div class="meta-row">
          <span class="meta-key">Category</span>
          <span class="meta-val">{category.replace('_', ' ').title()}</span>
        </div>
        <div class="meta-row">
          <span class="meta-key">Model</span>
          <span class="meta-val">XGBoost v1</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)