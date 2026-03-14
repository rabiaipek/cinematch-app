from fastapi import FastAPI
from recommender import MovieEngine

# Profesyonel Başlık
app = FastAPI(title="Movie Recommendation Engine API", version="1.0.0")
engine = MovieEngine()

@app.get("/")
def home():
    return {"status": "online", "project": "Movie Recommender AI by Rabia İPEK"}

# Buradaki yolu app.py'daki requests.get() ile uyumlu hale getirdik
@app.get("/recommend/{movie_id}")
def recommend(movie_id: int):
    sonuclar = engine.get_rec(movie_id)
    return {"oneriler": sonuclar}