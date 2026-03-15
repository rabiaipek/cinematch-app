from fastapi import FastAPI
from recommender import MovieEngine

app = FastAPI(title="CineMatch Hybrid AI API", version="2.0.0")
engine = MovieEngine()

@app.get("/")
def home():
    return {"status": "online", "mode": "Hybrid AI Enabled"}

# BURAYI DÜZELTTİK: user_id ve movie_id farklı olmalı
@app.get("/recommend/{user_id}/{movie_id}")
def recommend_hybrid(user_id: int, movie_id: int):
    try:
        sonuclar = engine.get_hybrid_rec(user_id, movie_id)
        return {"oneriler": sonuclar}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)