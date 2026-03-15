import streamlit as st
import requests
import pandas as pd

# 1. SAYFA KONFİGÜRASYONU
st.set_page_config(page_title="CineMatch AI | Smart Movie Discovery", page_icon="🎬", layout="wide")

APP_NAME = "CineMatch AI"

# 2. TEMA VE OTURUM YÖNETİMİ
if 'theme' not in st.session_state:
    st.session_state.theme = 'Koyu'
if 'selected_genre' not in st.session_state:
    st.session_state.selected_genre = None

# TMDB Afiş Fonksiyonu (Aynı bıraktık)
def get_movie_poster(movie_title):
    clean_title = movie_title.split(' (')[0]
    api_key = "8265bd1679663a7ea12ac168da84d2e8" 
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={clean_title}"
    try:
        response = requests.get(url).json()
        if response['results']:
            path = response['results'][0]['poster_path']
            return f"https://image.tmdb.org/t/p/w500{path}"
    except: pass
    return "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?q=80&w=300"

# 3. VERİ YÜKLEME
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/movies.csv")
        all_genres = set()
        df['genres'].str.split('|').apply(all_genres.update)
        return df, sorted([g for g in all_genres if g not in ["(no genres listed)", "IMAX", "Western", "War"]])
    except FileNotFoundError:
        st.error("Veri dosyası bulunamadı.")
        st.stop()

movies_df, genre_list = load_data()

# 4. RENK VE TEMA AYARLARI (Senin Ayarların)
if st.session_state.theme == 'Koyu':
    bg_c, txt_c, card_c = "#0A0C0F", "#FFFFFF", "#16191E"
    btn_bg, btn_txt, gold_c = "#E50914", "#FFFFFF", "#E50914" 
    overlay_c = "rgba(0, 0, 0, 0.75)"
    sidebar_bg = "#000000"
    title_color = "#FFFFFF"
else:
    bg_c, txt_c, card_c = "#F8F9FA", "#1A1A1B", "#FFFFFF" 
    btn_bg, btn_txt, gold_c = "#3498DB", "#FFFFFF", "#3498DB" 
    overlay_c = "rgba(255, 255, 255, 0.85)"
    sidebar_bg = "#F1F2F6"
    title_color = "#3498DB"

new_bg_img_url = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=1920"

# 5. CSS (Aynı bıraktık, User ID kutusu için küçük bir ekleme yaptık)
st.markdown(f"""
<style>
    .stApp {{
        background-image: url('{new_bg_img_url}');
        background-size: cover; background-attachment: fixed;
    }}
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: {overlay_c}; backdrop-filter: blur(5px); z-index: -1;
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }}
    /* Input kutularını daha şık yapalım */
    .stNumberInput div[data-baseweb="input"] {{
        background-color: #16191E !important;
        color: white !important;
        border-radius: 8px !important;
    }}
    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 8px !important;
    }}
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {btn_txt} !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 45px;
    }}
    .movie-card {{
        background-color: {card_c}; padding: 12px; border-radius: 18px;
        text-align: center; border: 1px solid rgba(128,128,128,0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3); height: 420px;
        display: flex; flex-direction: column; justify-content: space-between;
        color: {txt_c} !important;
    }}
    .poster-img {{ width: 100%; height: 280px; border-radius: 12px; object-fit: cover; }}
    .main-title {{ font-size: 60px; font-weight: 900; color: {title_color} !important; text-align: center; margin-bottom: 5px; }}
    .section-title {{ font-size: 24px; font-weight: bold; color: {txt_c}; border-left: 5px solid {gold_c}; padding-left: 10px; }}
</style>
""", unsafe_allow_html=True)

# 6. SIDEBAR İÇERİĞİ (YENİ KISIM BURADA)
with st.sidebar:
    st.markdown(f"<h2 style='color: white;'>⚙️ {APP_NAME}</h2>", unsafe_allow_html=True)
    
    # TEMA DEĞİŞTİRİCİ
    if st.button("☀️ Işığı Aç" if st.session_state.theme == 'Koyu' else "🌙 Karanlığa Geç"):
        st.session_state.theme = 'Açık' if st.session_state.theme == 'Koyu' else 'Koyu'
        st.rerun()
    
    st.markdown("---")
    
    # KULLANICI GİRİŞİ (YENİ EKLENEN)
    st.markdown("<b style='color: white;'>👤 Kullanıcı Kimliği:</b>", unsafe_allow_html=True)
    user_id = st.number_input("Kullanıcı ID", min_value=1, value=1, step=1, label_visibility="collapsed")
    st.caption("AI önerileri bu ID'ye göre kişiselleştirilir.")
    
    st.markdown("---")
    st.markdown("<b style='color: white;'>🔍 Beğendiğiniz Filmi Seçin:</b>", unsafe_allow_html=True)
    selected_movie = st.selectbox("", movies_df['title'].values, label_visibility="collapsed")
    
    st.write("") 
    recommend_button = st.button("Benzer Filmleri Bul 🚀", use_container_width=True)
    
    if st.button("🏠 Ana Sayfa", use_container_width=True):
        st.session_state.selected_genre = None
        st.rerun()
    
    st.markdown("---")
    st.success(f"Mod: Hibrit AI (NCF + Content)")
    st.caption(f"© 2026 {APP_NAME}")

# 7. ANA İÇERİK
if not recommend_button:
    st.markdown(f"<div class='main-title'>{APP_NAME}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{txt_c}; opacity:0.8;'>Kişiselleştirilmiş Film Deneyimi</p>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='section-title'>📽️ Kategoriler</div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, genre in enumerate(genre_list[:8]):
        with cols[i % 4]:
            if st.button(genre, key=f"btn_{genre}", use_container_width=True):
                st.session_state.selected_genre = genre

    if st.session_state.selected_genre:
        st.markdown(f"<div class='section-title'>🔥 {st.session_state.selected_genre} Seçkisi</div>", unsafe_allow_html=True)
        filtered_movies = movies_df[movies_df['genres'].str.contains(st.session_state.selected_genre)].head(5)
        res_cols = st.columns(5)
        for i, (idx, row) in enumerate(filtered_movies.iterrows()):
            with res_cols[i]:
                poster = get_movie_poster(row['title'])
                st.markdown(f'<div class="movie-card"><img src="{poster}" class="poster-img"><br><b>{row["title"].split(" (")[0]}</b></div>', unsafe_allow_html=True)
    else:
        st.markdown("<div class='section-title'>🌟 Öne Çıkanlar</div>", unsafe_allow_html=True)
        pop_cols = st.columns(5)
        for i, (idx, row) in enumerate(movies_df.sample(5).iterrows()):
            with pop_cols[i]:
                poster = get_movie_poster(row['title'])
                st.markdown(f'<div class="movie-card"><img src="{poster}" class="poster-img"><br><b>{row["title"].split(" (")[0]}</b></div>', unsafe_allow_html=True)

else:
    # BURASI ARTIK HİBRİT ÇALIŞIYOR
    # BURASI ARTIK YEREL BACKEND'E BAĞLI
    movie_id = movies_df[movies_df['title'] == selected_movie]['movieId'].values[0]
    try:
        # Kendi bilgisayarındaki FastAPI'ye (8000 portu) istek atıyoruz
        response = requests.get(f"http://127.0.0.1:8000/recommend/{user_id}/{movie_id}")
        oneriler = response.json()["oneriler"]
        
        st.markdown(f"<div class='section-title'>🎯 '{selected_movie}' Sevenler & {user_id}. Kullanıcı İçin</div>", unsafe_allow_html=True)
        cols = st.columns(5)
        for i, film in enumerate(oneriler[:5]):
            with cols[i]:
                p_url = get_movie_poster(film['title'])
                st.markdown(f'<div class="movie-card"><img src="{p_url}" class="poster-img"><br><b>{film["title"].split(" (")[0]}</b></div>', unsafe_allow_html=True)
    except Exception as e: 
        st.error(f"Bağlantı Hatası: {e}")