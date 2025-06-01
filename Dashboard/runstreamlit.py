import streamlit as st
from recommender import get_counter_heroes

# Setup halaman
st.set_page_config(page_title="MLBB Counter Hero", layout="wide")

# CSS Custom Styles
st.markdown("""
    <style>
        .main {
            background-color: #ffff !important;
        }
        body {
            background-color: #ffff !important;
        }
        .title {
            font-size: 42px;
            font-weight: bold;
            color: #e2adff;
            margin-bottom: 10px;
        }
        .sub-title {
            font-size: 22px;
            color: #e2adff;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #e9c2ff;
            color: #7d31a8;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-size: 16px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ffffff;
            color: #7d31a8;
        }
        .stSelectbox label {
            color: #e2adff !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Judul
st.markdown('<div class="title">🛡️ Mobile Legends Counter Hero Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Pilih 3 hero musuh yang ingin dianalisis:</div>', unsafe_allow_html=True)

# Daftar hero
hero_list = [
    "Layla", "Zilong", "Nana", "Gusion", "Chou", "Natalia",
    "Eudora", "Aurora", "Akai", "Saber", "Helcurt", "Valir"
]

# Dropdown input
col1, col2, col3 = st.columns(3)
with col1:
    hero1 = st.selectbox("🧟‍♂️ Hero Musuh 1", hero_list, key="hero1")
with col2:
    hero2 = st.selectbox("🧟‍♂️ Hero Musuh 2", hero_list, key="hero2")
with col3:
    hero3 = st.selectbox("🧟‍♂️ Hero Musuh 3", hero_list, key="hero3")

# Tombol rekomendasi
if st.button("🔍 Tampilkan Rekomendasi Hero Counter"):
    results = get_counter_heroes(hero1, hero2, hero3)
    st.markdown("## 🧠 Rekomendasi Counter Hero")
    for hero, winrate in results:
        st.markdown(f"- **{hero}** — Winrate: **{winrate}%**")
