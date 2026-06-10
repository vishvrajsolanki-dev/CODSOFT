import streamlit as st
from predict import predict_genre

st.set_page_config(
    page_title="PlotSense — Movie Genre AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:ital,wght@0,400;0,500;1,400&display=swap');

/* ── RESET & BASE ─────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body { margin: 0; padding: 0; }

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
section[data-testid="stAppViewContainer"],
.main {
    background: #0F0F17 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #C8C8D8 !important;
}

/* Kill all streamlit chrome */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu, footer, header,
.stDeployButton { display: none !important; visibility: hidden !important; }

/* Wide layout — centered column with side gutter */
.main .block-container {
    max-width: 860px !important;
    margin: 0 auto !important;
    padding: 0 2rem 5rem !important;
}

/* Force text color globally — fixes invisible fonts */
p, span, div, label, h1, h2, h3, h4, h5, h6, li, td, th {
    color: #C8C8D8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── BACKGROUND GRAIN TEXTURE ─────────────────── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(245,197,24,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 10% 80%, rgba(100,80,200,0.04) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ── HERO ─────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 5rem 1rem 3rem;
    position: relative;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(245,197,24,0.07);
    border: 1px solid rgba(245,197,24,0.18);
    border-radius: 100px;
    padding: 5px 16px 5px 10px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #C8A010 !important;
    margin-bottom: 1.4rem;
}

.badge-dot {
    width: 7px; height: 7px;
    background: #F5C518;
    border-radius: 50%;
    flex-shrink: 0;
    animation: blink 2.4s ease-in-out infinite;
}
@keyframes blink {
    0%,100% { opacity:1; } 50% { opacity:0.25; }
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 4.4rem !important;
    font-weight: 700 !important;
    line-height: 1.02 !important;
    letter-spacing: -2.5px !important;
    color: #FFFFFF !important;
    margin: 0 0 0.8rem !important;
}

.hero-title .gold { color: #F5C518 !important; }
.hero-title .dim  { color: #2A2A3E !important; }

.hero-desc {
    font-size: 1.05rem !important;
    color: #6A6A82 !important;
    line-height: 1.65 !important;
    max-width: 500px;
    margin: 0 auto 2.2rem !important;
    font-weight: 400 !important;
}

/* Film reel strip */
.filmstrip {
    display: flex;
    justify-content: center;
    gap: 4px;
    margin-bottom: 0.5rem;
}
.fc { width: 20px; height: 13px; background: #181828; border-radius: 3px; }
.fc.on { background: #F5C518; }
.fc.half { background: #2A2210; }

/* ── STATS BAR ────────────────────────────────── */
.stats-bar {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border: 1px solid #1C1C2C;
    border-radius: 14px;
    overflow: hidden;
    margin: 2.2rem 0 2rem;
    background: #131320;
}

.stat-item {
    padding: 1.6rem 1rem;
    text-align: center;
    border-right: 1px solid #1C1C2C;
}
.stat-item:last-child { border-right: none; }

.stat-num {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #F5C518 !important;
    letter-spacing: -1px !important;
    line-height: 1 !important;
}

.stat-lbl {
    font-size: 0.62rem !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #3A3A55 !important;
    margin-top: 6px !important;
}

/* ── FIELD LABELS ─────────────────────────────── */
.field-label {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.62rem !important;
    font-weight: 700 !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: #4A4A65 !important;
    margin-bottom: 0.55rem !important;
}
.field-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1C1C2C;
}

/* ── SELECTBOX ────────────────────────────────── */
.stSelectbox > div > div,
.stSelectbox [data-baseweb="select"] > div {
    background: #131320 !important;
    border: 1px solid #222235 !important;
    border-radius: 10px !important;
    color: #C8C8D8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
}

/* ── TEXTAREA ─────────────────────────────────── */
.stTextArea textarea {
    background: #131320 !important;
    border: 1px solid #222235 !important;
    border-radius: 12px !important;
    color: #D8D8E8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.97rem !important;
    line-height: 1.75 !important;
    padding: 1.1rem 1.3rem !important;
    caret-color: #F5C518 !important;
    resize: none !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.stTextArea textarea:focus {
    border-color: rgba(245,197,24,0.45) !important;
    box-shadow: 0 0 0 3px rgba(245,197,24,0.05) !important;
}

.stTextArea textarea::placeholder {
    color: #252535 !important;
    font-style: italic !important;
}

/* ── CHAR COUNT ───────────────────────────────── */
.char-count {
    font-size: 0.69rem !important;
    color: #2E2E45 !important;
    text-align: right !important;
    margin-top: -0.2rem !important;
    margin-bottom: 0.6rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0.5px !important;
}

/* ── PREDICT BUTTON ───────────────────────────── */
.stButton > button {
    background: #F5C518 !important;
    color: #0A0A10 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.83rem !important;
    letter-spacing: 2px !important;
    padding: 0.85rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    text-transform: uppercase !important;
    transition: background 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover {
    background: #FFD340 !important;
    box-shadow: 0 0 32px rgba(245,197,24,0.22) !important;
}

/* ── RESULT ───────────────────────────────────── */
.result-wrap { margin-top: 1.4rem; animation: fadeUp 0.35s ease; }

@keyframes fadeUp {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0); }
}

.result-card {
    background: #131320;
    border: 1px solid #1C1C2C;
    border-top: 2px solid #F5C518;
    border-radius: 14px;
    padding: 2rem 2.2rem;
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 90px;
    background: radial-gradient(ellipse at 50% -30%, rgba(245,197,24,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.result-eyebrow {
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: #3A3A55 !important;
    margin-bottom: 0.5rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.result-genre {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 700 !important;
    color: #F5C518 !important;
    letter-spacing: -1.5px !important;
    line-height: 1 !important;
    margin-bottom: 1.3rem !important;
}

.pills { display: flex; gap: 8px; flex-wrap: wrap; }

.pill {
    background: #0F0F1A;
    border: 1px solid #1C1C2C;
    border-radius: 6px;
    padding: 4px 11px;
    font-size: 0.68rem !important;
    color: #3E3E58 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0.3px;
}

/* ── WARNING ──────────────────────────────────── */
div[data-testid="stAlert"] {
    background: rgba(245,197,24,0.05) !important;
    border: 1px solid rgba(245,197,24,0.15) !important;
    border-radius: 10px !important;
}
div[data-testid="stAlert"] p { color: #907010 !important; }

/* ── SECTION DIVIDER ──────────────────────────── */
.sdiv {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1C1C2C 30%, #1C1C2C 70%, transparent);
    margin: 1.8rem 0;
}

/* ── FOOTER ───────────────────────────────────── */
.site-footer {
    text-align: center;
    padding-top: 2rem;
    margin-top: 4rem;
    border-top: 1px solid #131320;
}
.footer-name {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    color: #2A2A40 !important;
}
.footer-meta {
    font-size: 0.68rem !important;
    color: #1E1E2E !important;
    margin-top: 4px !important;
    letter-spacing: 0.4px !important;
}
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────
GENRE_ICONS = {
    "action":"💥","adventure":"🗺️","animation":"🎨","biography":"📖",
    "comedy":"😄","crime":"🔫","documentary":"🎙️","drama":"🎭",
    "family":"👨‍👩‍👧","fantasy":"🧙","game-show":"🎮","history":"🏛️",
    "horror":"👻","music":"🎵","musical":"🎼","mystery":"🔍",
    "news":"📰","reality-tv":"📺","romance":"❤️","sci-fi":"🚀",
    "short":"⏱️","sport":"⚽","talk-show":"🎤","thriller":"😰",
    "war":"⚔️","western":"🤠","adult":"🔞"
}

EXAMPLES = {
    "— pick a genre to load —": "",
    "⚡  Action":      "A retired black-ops soldier must race across three continents to dismantle a shadow organization that framed him for a political assassination and kidnapped his daughter.",
    "🚀  Sci-Fi":      "In 2157, a rogue AI controlling the global power grid demands a human sacrifice every 24 hours — and the engineer who built it is the only one who can shut it down.",
    "❤️  Romance":     "Two rival food critics, forced to share a tiny Paris apartment for a weekend assignment, discover their fiercest arguments are hiding something far more dangerous.",
    "👻  Horror":      "A rural family starts receiving voicemails from their deceased grandmother — messages that describe, in perfect detail, events that haven't happened yet.",
    "😄  Comedy":      "A strait-laced tax auditor accidentally enrolls in a professional clown academy and must survive a full week of classes to retrieve his stolen briefcase.",
    "🎙️  Documentary": "Three generations of fishermen on a remote Norwegian island reckon with the collapse of their way of life as warming seas push the fish deeper and further away.",
    "🎭  Drama":       "A celebrated concert pianist returns to her hometown after twenty years to settle her estranged father's estate — and uncovers the lie that drove her away.",
    "🔍  Mystery":     "When a famous novelist is found dead in a locked cabin with no footprints in the snow, the detective realizes every clue points directly at herself.",
}

# ── HERO ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge"><span class="badge-dot"></span>CodSoft ML Internship &nbsp;·&nbsp; Task 1</div>
  <h1 class="hero-title">Plot<span class="gold">Sense</span><span class="dim">.</span></h1>
  <p class="hero-desc">
    Paste any movie plot and watch the model decide its genre —
    Logistic Regression trained on 54,214 IMDB titles across 27 categories.
  </p>
  <div class="filmstrip">
    <div class="fc on"></div><div class="fc"></div><div class="fc on"></div>
    <div class="fc on"></div><div class="fc half"></div><div class="fc on"></div>
    <div class="fc"></div><div class="fc on"></div><div class="fc on"></div>
    <div class="fc half"></div><div class="fc on"></div><div class="fc"></div>
    <div class="fc on"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
  <div class="stat-item">
    <div class="stat-num">54,214</div>
    <div class="stat-lbl">Training Samples</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">58.7%</div>
    <div class="stat-lbl">Test Accuracy</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">27</div>
    <div class="stat-lbl">Genre Classes</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)

# ── EXAMPLES ──────────────────────────────────────────────────────
st.markdown('<p class="field-label">Quick Examples</p>', unsafe_allow_html=True)
selected = st.selectbox("Quick Examples", options=list(EXAMPLES.keys()), label_visibility="collapsed")
default_text = EXAMPLES[selected]

# ── PLOT INPUT ────────────────────────────────────────────────────
st.markdown('<p class="field-label" style="margin-top:1.1rem">Plot Summary</p>', unsafe_allow_html=True)
plot_input = st.text_area(
    "Plot Summary",
    value=default_text,
    height=170,
    placeholder="Paste or write a movie plot summary here...\n\ne.g. A detective is called to investigate a locked-room murder at a remote lighthouse — and the only suspect is the storm.",
    label_visibility="collapsed"
)

char_count = len(plot_input.strip())
if char_count > 0:
    st.markdown(f'<p class="char-count">{char_count} characters</p>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

# ── PREDICT ───────────────────────────────────────────────────────
if st.button("PREDICT GENRE", use_container_width=True):
    if plot_input.strip():
        with st.spinner("Analyzing plot..."):
            genre = predict_genre(plot_input.strip())

        genre_key = genre.strip().lower()
        icon = GENRE_ICONS.get(genre_key, "🎬")
        genre_display = genre.strip().upper()

        st.markdown(f"""
        <div class="result-wrap">
          <div class="result-card">
            <p class="result-eyebrow">Predicted Genre</p>
            <p class="result-genre">{icon}&nbsp; {genre_display}</p>
            <div class="pills">
              <span class="pill">Logistic Regression</span>
              <span class="pill">TF-IDF · 10k features</span>
              <span class="pill">IMDB Dataset</span>
              <span class="pill">scikit-learn · NLTK</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Enter a plot summary first.")

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
  <p class="footer-name">PlotSense AI</p>
  <p class="footer-meta">CodSoft ML Internship &nbsp;·&nbsp; Built by Vishvrajsinh Solanki &nbsp;·&nbsp; Logistic Regression + TF-IDF · NLTK · Streamlit</p>
</div>
""", unsafe_allow_html=True)