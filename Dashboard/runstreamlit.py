import streamlit as st
from recommender import get_counter_heroes, get_model_metrics

# Konfigurasi halaman
st.set_page_config(page_title="Hero Recommendation", layout="centered")

# Load data hero dari CSV
hero_list = [
    'Aamon', 'Akai', 'Aldous', 'Alice', 'Alpha', 'Alucard', 'Angela', 'Argus', 'Arlott', 'Aurora',
    'Aulus', 'Atlas', 'Badang', 'Balmond', 'Barats', 'Baxia', 'Beatrix', 'Belerick', 'Benedetta',
    'Brody', 'Bruno', 'Carmilla', 'Cecilion', 'Chang\'e', 'Chou', 'Claude', 'Clint', 'Cyclops',
    'Diggie', 'Dyrroth', 'Edith', 'Esmeralda', 'Estes', 'Eudora', 'Fanny', 'Faramis', 'Floryn',
    'Franco', 'Fredrinn', 'Freya', 'Gatotkaca', 'Gloo', 'Gord', 'Granger', 'Grock', 'Gusion',
    'Guinevere', 'Hanabi', 'Hanzo', 'Harith', 'Harley', 'Hayabusa', 'Helcurt', 'Hilda', 'Hylos',
    'Irithel', 'Jawhead', 'Johnson', 'Joy', 'Julian', 'Kadita', 'Kagura', 'Kaja', 'Karina', 'Karrie',
    'Khaleed', 'Khufra', 'Kimmy', 'Lancelot', 'Layla', 'Leomord', 'Lesley', 'Ling', 'Lolita',
    'Lunox', 'Luo Yi', 'Lylia', 'Mathilda', 'Martis', 'Masha', 'Melissa', 'Minotaur', 'Minsitthar',
    'Miya', 'Moskov', 'Natalia', 'Natan', 'Nana', 'Novaria', 'Odette', 'Paquito', 'Pharsa',
    'Phoveus', 'Popol and Kupa', 'Roger', 'Ruby', 'Saber', 'Selena', 'Silvanna', 'Sun', 'Terizla',
    'Thamuz', 'Tigreal', 'Uranus', 'Vale', 'Valentina', 'Valir', 'Vexana', 'Wanwan', 'X.Borg',
    'Xavier', 'Yi Sun-shin', 'Yin', 'Yve', 'Yu Zhong', 'Zilong', 'Zhask'
]


# CSS Styling: Flexbox layout untuk metrik
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .metrics-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 3rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    .metric-card {
        background: transparent;
        padding: 1rem;
        text-align: center;
        border-radius: 10px;
        min-width: 120px;
    }
    .metric-title {
        font-size: 1rem;
        color: #cccccc;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Judul halaman
st.markdown("<h1 style='text-align: center;'>Analisis Hero Mobile Legends⚔️</h1>", unsafe_allow_html=True)

# Ambil metrik
accuracy, roc_auc, cv_score, _ = get_model_metrics()

# Tampilkan metrik dalam baris horizontal
st.markdown(f"""
<div class="metrics-container">
    <div class="metric-card">
        <div class="metric-title">📊 Accuracy</div>
        <div class="metric-value">{accuracy:.0f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">🧠 ROC AUC</div>
        <div class="metric-value">{roc_auc:.0f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">📌 Cross-validation</div>
        <div class="metric-value">{cv_score:.0f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Input
st.subheader("Input")
enemy1 = st.selectbox(" 🦹🏻‍♀️ Enemy Hero 1 🦹🏻‍♂️", hero_list)
enemy2 = st.selectbox("🦹🏻‍♀️ Enemy Hero 2 🦹🏻‍♂️", hero_list)
enemy3 = st.selectbox("🦹🏻‍♀️ Enemy Hero 3 🦹🏻‍♂️", hero_list)

# Submit
if st.button("🫵🏻 Analisis "):
    if enemy1 and enemy2 and enemy3:
        recommendations = get_counter_heroes(enemy1, enemy2, enemy3)
        st.subheader("Rekomendasi Hero Counter")
        for i, (hero, score) in enumerate(recommendations, 1):
            st.markdown(f"**{i}. {hero}** – Prediksi kemenangan: {score:.2f}%")
    else:
        st.warning("Tolong pilih ketiga hero musuh terlebih dahulu!")
