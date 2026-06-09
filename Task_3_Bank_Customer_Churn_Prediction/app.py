import os
import streamlit as st
import joblib
import numpy as np

# ── Path fix for Streamlit Cloud ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model  = joblib.load(os.path.join(BASE_DIR, "models", "churn_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
le_geo = joblib.load(os.path.join(BASE_DIR, "models", "le_geo.pkl"))
le_gen = joblib.load(os.path.join(BASE_DIR, "models", "le_gen.pkl"))

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChurnSight | Retention Intelligence",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1a2e 40%, #091524 100%);
    min-height: 100vh;
}

/* ── Hide streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 780px; }

/* ── Header ── */
.brand-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.brand-logo {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #c8a96e;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.brand-logo span { color: #ffffff; }
.brand-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #f0f4ff;
    letter-spacing: -0.02em;
    margin: 0.25rem 0;
    line-height: 1.2;
}
.brand-subtitle {
    font-size: 0.9rem;
    color: #7a8ba8;
    font-weight: 400;
    margin-top: 0.4rem;
}

/* ── Section divider ── */
.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #c8a96e;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, #c8a96e33, transparent);
}

/* ── Glass card ── */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(12px);
}

/* ── Streamlit widget overrides ── */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #f0f4ff !important;
    transition: border-color 0.2s;
}
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within {
    border-color: #c8a96e !important;
    box-shadow: 0 0 0 2px rgba(200,169,110,0.18) !important;
}
div[data-baseweb="select"] svg { color: #c8a96e !important; }

.stSlider > div > div > div {
    background: #c8a96e !important;
}
.stSlider > div > div > div > div {
    background: #c8a96e !important;
    border: 2px solid #0d1a2e !important;
    box-shadow: 0 0 8px rgba(200,169,110,0.5) !important;
}

label[data-testid="stWidgetLabel"] p,
label[data-testid="stWidgetLabel"] {
    color: #a8bbd4 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    text-transform: uppercase !important;
}

/* ── Predict button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #c8a96e 0%, #b8934a 100%) !important;
    color: #0a0f1e !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.9rem 2rem !important;
    height: auto !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(200,169,110,0.3) !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #d4b87c 0%, #c8a96e 100%) !important;
    box-shadow: 0 6px 28px rgba(200,169,110,0.45) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Result card ── */
.result-card {
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-card.high {
    background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(220,38,38,0.06));
    border: 1px solid rgba(239,68,68,0.3);
}
.result-card.low {
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(5,150,105,0.06));
    border: 1px solid rgba(16,185,129,0.3);
}
.result-card.medium {
    background: linear-gradient(135deg, rgba(245,158,11,0.12), rgba(217,119,6,0.06));
    border: 1px solid rgba(245,158,11,0.3);
}
.risk-badge {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 1rem;
}
.badge-high { background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.badge-medium { background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.badge-low { background: rgba(16,185,129,0.2); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.risk-percentage {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1;
    margin: 0.5rem 0;
}
.pct-high { color: #f87171; }
.pct-medium { color: #fbbf24; }
.pct-low { color: #34d399; }
.risk-label {
    font-size: 0.88rem;
    color: #7a8ba8;
    margin-top: 0.5rem;
}
.risk-desc {
    font-size: 0.82rem;
    color: #a8bbd4;
    margin-top: 1rem;
    line-height: 1.6;
    max-width: 420px;
    margin-left: auto;
    margin-right: auto;
}

/* ── Gauge bar ── */
.gauge-track {
    background: rgba(255,255,255,0.08);
    border-radius: 99px;
    height: 8px;
    margin: 1.25rem auto;
    max-width: 360px;
    overflow: hidden;
}
.gauge-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
}
.fill-high { background: linear-gradient(to right, #f87171, #ef4444); }
.fill-medium { background: linear-gradient(to right, #fbbf24, #f59e0b); }
.fill-low { background: linear-gradient(to right, #34d399, #10b981); }

/* ── Footer ── */
.footer-note {
    text-align: center;
    font-size: 0.75rem;
    color: #3d4f66;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}

/* ── Number input arrows ── */
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button { opacity: 0.3; }

/* ── Metric row ── */
.metric-row {
    display: flex;
    gap: 12px;
    margin-bottom: 1rem;
}
.metric-chip {
    flex: 1;
    background: rgba(200,169,110,0.08);
    border: 1px solid rgba(200,169,110,0.18);
    border-radius: 10px;
    padding: 0.75rem;
    text-align: center;
}
.metric-chip .val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #c8a96e;
}
.metric-chip .lbl {
    font-size: 0.7rem;
    color: #7a8ba8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-header">
  <div class="brand-logo">⬡ <span>ChurnSight</span></div>
  <div class="brand-title">Customer Retention Intelligence</div>
  <div class="brand-subtitle">Predict churn risk from customer profile data — powered by Gradient Boosting</div>
</div>
""", unsafe_allow_html=True)

# ── Model stats strip ─────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-row">
  <div class="metric-chip"><div class="val">86.45%</div><div class="lbl">Accuracy</div></div>
  <div class="metric-chip"><div class="val">0.87</div><div class="lbl">ROC-AUC</div></div>
  <div class="metric-chip"><div class="val">10K</div><div class="lbl">Training Samples</div></div>
  <div class="metric-chip"><div class="val">GBM</div><div class="lbl">Model</div></div>
</div>
""", unsafe_allow_html=True)

# ── Section: Identity ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Customer Identity</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    geography = st.selectbox(
        "Country of Residence",
        le_geo.classes_,
        help="Customer's registered country"
    )
with col2:
    gender = st.selectbox(
        "Gender",
        le_gen.classes_,
    )

# ── Section: Financial Profile ─────────────────────────────────────────────────
st.markdown('<div class="section-label">Financial Profile</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    credit_score = st.slider("Credit Score", 300, 850, 650,
        help="Customer's credit score (300 = Poor, 850 = Excellent)")
with col4:
    age = st.slider("Age", 18, 92, 35)

col5, col6 = st.columns(2)
with col5:
    balance = st.number_input(
        "Account Balance ($)",
        min_value=0.0,
        max_value=300000.0,
        value=50000.0,
        step=1000.0,
        format="%.2f"
    )
with col6:
    salary = st.number_input(
        "Estimated Annual Salary ($)",
        min_value=0.0,
        max_value=300000.0,
        value=75000.0,
        step=1000.0,
        format="%.2f"
    )

# ── Section: Account Status ────────────────────────────────────────────────────
st.markdown('<div class="section-label">Account Status</div>', unsafe_allow_html=True)

col7, col8, col9, col10 = st.columns(4)
with col7:
    tenure = st.slider("Tenure (yrs)", 0, 10, 5,
        help="Years as a customer")
with col8:
    num_products = st.selectbox(
        "Products Held",
        options=[1, 2, 3, 4],
        index=0,
        help="Number of bank products the customer uses"
    )
with col9:
    has_cr_card = st.selectbox(
        "Credit Card",
        options=["Yes", "No"],
        help="Does the customer hold a credit card?"
    )
with col10:
    is_active = st.selectbox(
        "Active Member",
        options=["Yes", "No"],
        help="Is the customer actively using the account?"
    )

# ── Predict ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("Run Risk Analysis", use_container_width=True)

if predict_btn:
    geo_enc  = le_geo.transform([geography])[0]
    gen_enc  = le_gen.transform([gender])[0]
    cr_card  = 1 if has_cr_card == "Yes" else 0
    active   = 1 if is_active == "Yes" else 0

    features        = np.array([[credit_score, geo_enc, gen_enc, age, tenure,
                                  balance, num_products, cr_card, active, salary]])
    features_scaled = scaler.transform(features)
    prob            = model.predict_proba(features_scaled)[0][1]
    pct             = prob * 100

    if pct >= 60:
        tier, card_cls, badge_cls, pct_cls, fill_cls = (
            "High Risk", "high", "badge-high", "pct-high", "fill-high"
        )
        desc = "This customer profile shows strong churn signals. Immediate retention outreach — personalised offer or dedicated relationship manager contact — is recommended."
    elif pct >= 35:
        tier, card_cls, badge_cls, pct_cls, fill_cls = (
            "Medium Risk", "medium", "badge-medium", "pct-medium", "fill-medium"
        )
        desc = "Elevated risk detected. A proactive check-in or targeted loyalty incentive within the next 30 days could significantly reduce the likelihood of churn."
    else:
        tier, card_cls, badge_cls, pct_cls, fill_cls = (
            "Low Risk", "low", "badge-low", "pct-low", "fill-low"
        )
        desc = "Customer profile indicates healthy engagement. Routine relationship maintenance is sufficient — consider cross-sell opportunities for additional products."

    st.markdown(f"""
    <div class="result-card {card_cls}">
      <span class="risk-badge {badge_cls}">{tier}</span>
      <div class="risk-percentage {pct_cls}">{pct:.1f}%</div>
      <div class="risk-label">Estimated Churn Probability</div>
      <div class="gauge-track">
        <div class="gauge-fill {fill_cls}" style="width:{pct:.1f}%"></div>
      </div>
      <div class="risk-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
  ChurnSight · CodSoft ML Internship Task 3 · Model: GradientBoostingClassifier · Dataset: Churn Modelling (Kaggle)
</div>
""", unsafe_allow_html=True)