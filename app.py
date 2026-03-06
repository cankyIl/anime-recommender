import streamlit as st
import pandas as pd
import pickle
import urllib.parse

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Anime Recommender", page_icon="⛩️", layout="wide", initial_sidebar_state="expanded")

# --- UNIVERSAL CUSTOM CSS (MAC & WINDOWS FRIENDLY) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Oswald:wght@700&display=swap');

    .stApp {
        background-color: #1a1a24;
        background-image: radial-gradient(#3a3a4a 1px, transparent 1px);
        background-size: 20px 20px;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    h1 {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Oswald', sans-serif;
        text-transform: uppercase;
        text-shadow: 2px 2px 0px rgba(255, 75, 75, 0.2);
        letter-spacing: 2px;
    }
    
    .subtitle {
        text-align: center;
        font-size: clamp(1rem, 2vw, 1.2rem);
        color: #a3a8b8;
        margin-bottom: 2rem;
        font-style: italic;
    }

    .recommendation-card {
        background: rgba(38, 39, 48, 0.95);
        backdrop-filter: blur(5px);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #ff4b4b;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateY(-5px);
        border-color: #00ffcc;
    }

    .anime-title {
        margin: 0;
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 700;
    }

    .match-score {
        margin: 5px 0 15px 0;
        color: #00ffcc; 
        font-family: 'monospace';
        font-size: 0.95rem;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff4b4b 0%, #ff7676 100%);
        color: white !important;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: 700;
        text-transform: uppercase;
    }

    .mal-link {
        color: #1a1a24 !important;
        background-color: #00ffcc;
        padding: 6px 14px;
        border-radius: 20px;
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. LOAD DATA ---
@st.cache_data
def load_data():
    with open('collaborative_model.pkl', 'rb') as f:
        collab_df = pickle.load(f)
    with open('content_model.pkl', 'rb') as f:
        content_df = pickle.load(f)
    with open('anime_list.pkl', 'rb') as f:
        anime_list = pickle.load(f)
    return collab_df, content_df, anime_list

collab_df, content_df, anime_list = load_data()

# --- SIDEBAR: THE GUILD KIOSK ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00ffcc; font-family: Oswald;'>🎌 The Guild Kiosk</h2>", unsafe_allow_html=True)
    st.image("https://www.svgrepo.com/show/309875/ninja.svg", width=100) 
    
    # YOUR EXACT MESSAGE
    st.markdown("""
    The goal of this website is to combine my interest in math with my interest in anime. I wanted to make a website that uses a dataset from MAL(CooperUnions One) to match anime with anime you already like(based on either genre or user rating). This website uses Cosine similarity to power the recommendation engine. A plan for this website is to use a newer, more improved dataset or increase the number of ways to compare(it could be based on episodes as well).
    """)
    
    st.markdown("---")
    st.caption(f"📜 Archives Loaded: **{len(anime_list):,} Anime**")
    st.caption("⚙️ System Status: **Nominal**")
    st.caption("💥 Power Level: **OVER 9000**")

# --- 2. MATH LOGIC ---
def get_hybrid_recommendation(anime_name, alpha):
    try:
        if anime_name not in collab_df.columns or anime_name not in content_df.columns:
            return "NOT_FOUND"
        sim_collab = collab_df[anime_name]
        sim_content = content_df[anime_name]
        hybrid_scores = (sim_collab * alpha) + (sim_content * (1 - alpha))
        return hybrid_scores.sort_values(ascending=False).drop(anime_name, errors='ignore').head(5).to_dict()
    except:
        return None

# --- 3. UI LAYOUT ---
st.markdown("<h1> ⚔️ Anime Search Engine ⚔️ </h1>")
st.markdown("<p class='subtitle'>Powered by Linear Algebra & Magic</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.8])

with col1:
    st.subheader("🔮 Scrying Pool")
    selected_anime = st.selectbox("Select an anime to analyze:", anime_list)
    alpha = st.slider("0 = Genre Match | 1 = Rating Match", 0.0, 1.0, 0.5, 0.1)
    analyze_button = st.button("✨ INITIALIZE LINK START ✨")
    
    with st.expander("🧠 How does the math work?"):
        st.write("We use **Cosine Similarity** to measure the angle between vectors.")
        

with col2:
    st.subheader("🎯 Quest Board")
    if analyze_button:
        with st.spinner("Crunching matrices..."):
            recommendations = get_hybrid_recommendation(selected_anime, alpha)
        
        if recommendations == "NOT_FOUND":
            st.error("Anime not found in databanks.")
        elif recommendations:
            for anime, score in recommendations.items():
                m_percent = int(score * 100)
                safe_url = f"https://myanimelist.net/anime.php?q={urllib.parse.quote(str(anime))}&cat=anime"
                st.markdown(f"""
                    <div class="recommendation-card">
                        <div class="anime-title">📺 {anime}</div>
                        <div class="match-score">SYNC RATE: {m_percent}%</div>
                        <a href="{safe_url}" target="_blank" class="mal-link">VIEW ON MAL</a>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👈 Select a series to begin.")
