import os
import pickle
import streamlit as st
from utils import clean_text

st.set_page_config(
    page_title="CineGenre AI",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0A0A0F;
    color: #E8E8F0;
}

.stApp {
    background: #0A0A0F;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 760px;
}

.cinema-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid #1E1E2E;
    margin-bottom: 2rem;
}

.cinema-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #F5C518;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1;
}

.cinema-logo span {
    color: #FFFFFF;
}

.cinema-tagline {
    font-size: 0.85rem;
    color: #6B6B80;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-top: 0.5rem;
    font-weight: 400;
}

.film-strip {
    display: flex;
    justify-content: center;
    gap: 6px;
    margin-top: 1rem;
}

.film-cell {
    width: 18px;
    height: 12px;
    background: #1E1E2E;
    border-radius: 2px;
}

.film-cell.active {
    background: #F5C518;
}

.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6B6B80;
    margin-bottom: 0.6rem;
}

.stTextArea textarea {
    background: #12121C !important;
    border: 1px solid #2A2A3E !important;
    border-radius: 12px !important;
    color: #E8E8F0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    padding: 1rem 1.2rem !important;
    caret-color: #F5C518;
    transition: border-color 0.2s ease;
    resize: none !important;
}

.stTextArea textarea:focus {
    border-color: #F5C518 !important;
    box-shadow: 0 0 0 3px rgba(245, 197, 24, 0.08) !important;
}

.stTextArea textarea::placeholder {
    color: #3A3A52 !important;
    font-style: italic;
}

.stButton > button {
    background: #F5C518 !important;
    color: #0A0A0F !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: #FFD340 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(245, 197, 24, 0.25) !important;
}

.result-card {
    background: #12121C;
    border: 1px solid #2A2A3E;
    border-left: 3px solid #F5C518;
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    margin-top: 1.5rem;
}

.result-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #6B6B80;
    margin-bottom: 0.5rem;
    font-family: 'Space Grotesk', sans-serif;
}

.result-genre {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #F5C518;
    margin: 0;
    line-height: 1.1;
}

.result-meta {
    font-size: 0.8rem;
    color: #4A4A60;
    margin-top: 0.8rem;
    padding-top: 0.8rem;
    border-top: 1px solid #1E1E2E;
}

.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 1.5rem 0;
}

.stat-card {
    background: #12121C;
    border: 1px solid #1E1E2E;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}

.stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #F5C518;
}

.stat-label {
    font-size: 0.72rem;
    color: #6B6B80;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 3px;
}

.cinema-divider {
    border: none;
    border-top: 1px solid #1E1E2E;
    margin: 2rem 0;
}

.cinema-footer {
    text-align: center;
    color: #3A3A52;
    font-size: 0.75rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1E1E2E;
    letter-spacing: 0.5px;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

GENRE_ICONS = {
    "action": "💥", "adventure": "🗺️", "animation": "🎨", "biography": "📖",
    "comedy": "😄", "crime": "🔫", "documentary": "🎙️", "drama": "🎭",
    "family": "👨‍👩‍👧", "fantasy": "🧙", "game-show": "🎮", "history": "🏛️",
    "horror": "👻", "music": "🎵", "musical": "🎼", "mystery": "🔍",
    "news": "📰", "reality-tv": "📺", "romance": "❤️", "sci-fi": "🚀",
    "short": "⏱️", "sport": "⚽", "talk-show": "🎤", "thriller": "😰",
    "war": "⚔️", "western": "🤠", "adult": "🔞"
}

EXAMPLE_PLOTS = {
    "Action": "A retired special forces operative goes on a violent rampage through a city to rescue his kidnapped daughter from a ruthless crime syndicate.",
    "Sci-Fi": "In a dystopian future, a rogue scientist discovers that human consciousness can be uploaded to a digital realm, blurring the line between life and death.",
    "Romance": "Two strangers meet by chance on a train across Europe and spend 24 hours together, falling deeply in love despite their vastly different lives.",
    "Horror": "A family moves into a remote farmhouse only to discover that the previous owners were brutally murdered and whatever killed them never left.",
    "Comedy": "A bumbling accountant accidentally becomes the most wanted man in three countries after mistakenly picking up a briefcase full of stolen diamonds.",
    "Documentary": "Filmmakers spend three years embedded with a remote indigenous tribe in the Amazon, documenting their ancient traditions and fight against deforestation.",
}

@st.cache_resource
def load_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE_DIR, 'models', 'model.pkl'), 'rb') as f:
        model = pickle.load(f)
    with open(os.path.join(BASE_DIR, 'models', 'vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

model, vectorizer = load_model()

def predict_genre(plot_summary):
    cleaned = clean_text(plot_summary)
    vec = vectorizer.transform([cleaned])
    return model.predict(vec)[0]

st.markdown("""
<div class="cinema-header">
    <p class="cinema-logo">CINE<span>GENRE</span> <span style="color:#F5C518">AI</span></p>
    <p class="cinema-tagline">Machine Learning · Plot Intelligence · 27 Genres</p>
    <div class="film-strip">
        <div class="film-cell active"></div>
        <div class="film-cell"></div>
        <div class="film-cell active"></div>
        <div class="film-cell active"></div>
        <div class="film-cell"></div>
        <div class="film-cell active"></div>
        <div class="film-cell"></div>
        <div class="film-cell active"></div>
        <div class="film-cell active"></div>
        <div class="film-cell"></div>
        <div class="film-cell active"></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-value">54,214</div>
        <div class="stat-label">Training Samples</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">60.25%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">27</div>
        <div class="stat-label">Genres</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="cinema-divider">', unsafe_allow_html=True)

st.markdown('<p class="section-label">Quick Examples</p>', unsafe_allow_html=True)

selected_example = st.selectbox(
    "Load an example plot",
    options=["— select a genre —"] + list(EXAMPLE_PLOTS.keys()),
    label_visibility="collapsed"
)

if selected_example != "— select a genre —":
    default_text = EXAMPLE_PLOTS[selected_example]
else:
    default_text = ""

st.markdown('<p class="section-label" style="margin-top:1.2rem">Plot Summary</p>', unsafe_allow_html=True)

plot_input = st.text_area(
    "Plot Summary",
    value=default_text,
    height=160,
    placeholder="Paste or type a movie plot summary here...\n\ne.g. A seasoned detective is drawn into a web of deceit when a mysterious woman walks into his office with a story too dangerous to ignore.",
    label_visibility="collapsed"
)

char_count = len(plot_input.strip())
if char_count > 0:
    st.markdown(f'<p style="font-size:0.72rem; color:#3A3A52; text-align:right; margin-top:-0.5rem;">{char_count} characters</p>', unsafe_allow_html=True)

st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

predict_btn = st.button("PREDICT GENRE", use_container_width=True)

if predict_btn:
    if plot_input.strip():
        with st.spinner("Analyzing plot..."):
            genre = predict_genre(plot_input.strip())

        genre_clean = genre.strip().lower()
        icon = GENRE_ICONS.get(genre_clean, "🎬")
        genre_display = genre.strip().upper()

        st.markdown(f"""
        <div class="result-card">
            <p class="result-label">Predicted Genre</p>
            <p class="result-genre">{icon} {genre_display}</p>
            <p class="result-meta">
                Model: Logistic Regression &nbsp;·&nbsp; Vectorizer: TF-IDF (50k features) &nbsp;·&nbsp; Trained on IMDB dataset
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please enter a plot summary before predicting.")

st.markdown("""
<div class="cinema-footer">
    CineGenre AI &nbsp;·&nbsp; CodSoft ML Internship &nbsp;·&nbsp; Built by Vishvrajsinh Solanki
    <br>Logistic Regression + TF-IDF &nbsp;·&nbsp; scikit-learn · NLTK · Streamlit
</div>
""", unsafe_allow_html=True)