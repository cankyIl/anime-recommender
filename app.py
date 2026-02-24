import streamlit as st
import pandas as pd
import pickle
import urllib.parse

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Anime Recommender", page_icon="⛩️", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR DECORATION ---
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a24;
        background-image: radial-gradient(#3a3a4a 1px, transparent 1px);
        background-size: 20px 20px;
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Impact', sans-serif;
        text-transform: uppercase;
        text-shadow: 3px 3px 0px rgba(255, 75, 75, 0.3);
        letter-spacing: 3px;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #a3a8b8;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .recommendation-card {
        background: linear-gradient(145deg, #262730, #1e1f26);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 15px;
        border-left: 5px solid #ff4b4b;
        border-right: 2px solid #ff4b4b;
        transition: transform 0.2s ease-in-out, border-color 0.2s ease;
    }
    .recommendation-card:hover {
        transform: scale(1.02);
        border-left: 5px solid #00ffcc; 
        border-right: 5px solid #00ffcc;
    }
    .anime-title {
        margin: 0;
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: bold;
    }
    .match-score {
        margin: 0;
        color: #00ffcc; 
        font-size: 1rem;
        padding-bottom: 8px;
        text-shadow: 0 0 5px rgba(0, 255, 204, 0.3);
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff4b4b, #ff7676);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(255, 75, 75, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.8);
        transform: translateY(-2px);
    }
    .mal-link {
        color: white;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        margin-top: 5px;
        padding: 5px 10px;
        background-color: #ff4b4b;
        border-radius: 5px;
        transition: background-color 0.2s ease;
    }
    .mal-link:hover {
        background-color: #00ffcc;
        color: #1a1a24;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. LOAD THE REAL BRAIN (Moved up!) ---
@st.cache_data
def load_data():
    with open('collaborative_model.pkl', 'rb') as f:
        collab_df = pickle.load(f)
    with open('content_model.pkl', 'rb') as f:
        content_df = pickle.load(f)
    with open('anime_list.pkl', 'rb') as f:
        anime_list = pickle.load(f)
    return collab_df, content_df, anime_list

# We load the data here so the Sidebar can read the length of anime_list
collab_df, content_df, anime_list = load_data()

# --- SIDEBAR: THE GUILD KIOSK ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00ffcc;'>🎌 The Guild Kiosk</h2>", unsafe_allow_html=True)
    st.image("https://www.svgrepo.com/show/309875/ninja.svg", width=120) 
    st.markdown("""
    **Welcome, Traveler!** I am your UI navigator. Enter your favorite series, and I'll tap into the World Tree's databanks to find your next adventure.
    """)
    st.markdown("---")
    
    # NEW: Dynamically counting the dataset size! The {:,} adds commas for large numbers (e.g., 7,000).
    st.caption(f"📜 Archives Loaded: **{len(anime_list):,} Anime**")
    
    st.caption("⚙️ System Status: All Systems Nominal")
    st.caption("💥 Power Level: OVER 9000!")

# --- 2. THE ACTUAL MATH LOGIC ---
def get_hybrid_recommendation(anime_name, alpha):
    try:
        if anime_name not in collab_df.columns or anime_name not in content_df.columns:
            return "NOT_FOUND"
            
        sim_scores_collab = collab_df[anime_name]
        sim_scores_content = content_df[anime_name]
        hybrid_scores = (sim_scores_collab * alpha) + (sim_scores_content * (1 - alpha))
        
        top_matches = hybrid_scores.sort_values(ascending=False).drop(anime_name, errors='ignore').head(5)
        return top_matches.to_dict()
    except Exception as e:
        return None

# --- 3. THE WEBSITE UI ---
st.markdown("<h1> ⚔️ Anime Search Engine ⚔️ </h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Powered by Linear Algebra & Magic</p>", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔮 Scrying Pool (Settings)")
    selected_anime = st.selectbox("Select an anime to analyze:", anime_list)
    
    st.write("") 
    st.markdown("**Algorithm Balance:**")
    alpha = st.slider(
        "0 = Pure Genre Match, 1 = Pure Rating Match", 
        min_value=0.0, max_value=1.0, value=0.5, step=0.1
    )
    
    st.write("") 
    analyze_button = st.button("✨ INITIALIZE LINK START ✨", use_container_width=True)
    
    st.write("") 
    
    with st.expander("🧠 How does the math work?"):
        st.write("""
            This engine uses **Cosine Similarity** to compare multi-dimensional vectors from the Cooper Union dataset.
            - **Content Score:** Analyzes genre overlap using One-Hot Encoding.
            - **Collaborative Score:** Analyzes user rating patterns across thousands of users.
            - The slider adjusts the weight between these two matrices!
        """)

with col2:
    st.subheader("🎯 Quest Board (Matches)")
    
    if analyze_button:
        with st.spinner("Crunching the matrices..."):
            recommendations = get_hybrid_recommendation(selected_anime, alpha)
        
        if recommendations == "NOT_FOUND":
            st.error(f"Anime '{selected_anime}' not found in the matrix columns. Check for mismatched text formatting in your datasets!")
        elif recommendations is not None:
            for anime, score in recommendations.items():
                match_percent = int(score * 100)
                safe_name = urllib.parse.quote(str(anime))
                mal_url = f"https://myanimelist.net/anime.php?q={safe_name}&cat=anime"
                
                st.markdown(f"""
                    <div class="recommendation-card">
                        <p class="anime-title">📺 {anime}</p>
                        <p class="match-score">Synchronization Rate: <strong>{match_percent}%</strong></p>
                        <a href="{mal_url}" target="_blank" class="mal-link">🔗 View on MyAnimeList</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Oops! Something went wrong calculating the vectors. Check your terminal for errors.")
    else:
        st.info("👈 Select an anime and hit 'LINK START' to see your recommendations!")