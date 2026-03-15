import pandas as pd
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
from model_arch import NCFModel # Az önce oluşturduğumuz mimari

class MovieEngine:
    def __init__(self):
        print("Backend: Hibrit model ve veriler yukleniyor...")
        self.movies = pd.read_csv("data/movies.csv")
        self.ratings = pd.read_csv("data/ratings.csv")
        
        # --- 1. SENİN VERİ ÖN İŞLEME MANTIĞIN (KORUDUK) ---
        user_counts = self.ratings['userId'].value_counts()
        active_users = user_counts[user_counts >= 20].index
        self.ratings = self.ratings[self.ratings['userId'].isin(active_users)]
        
        movie_counts = self.ratings['movieId'].value_counts()
        popular_movies = movie_counts[movie_counts >= 5].index
        self.ratings = self.ratings[self.ratings['movieId'].isin(popular_movies)]
        
        # --- 2. MATRİS VE COSINE SİMİLARİTY (KLASİK KATMAN) ---
        user_movie_matrix = self.ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
        item_similarity = cosine_similarity(user_movie_matrix.T)
        self.similarity_df = pd.DataFrame(item_similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)
        
        # --- 3. DEEP LEARNING (NCF) KATMANI ---
        num_users = self.ratings['userId'].max() + 1
        num_items = self.ratings['movieId'].max() + 1
        self.dl_model = NCFModel(num_users, num_items)
        
        try:
            # Eğittiğimiz modelin ağırlıklarını yüklüyoruz
            self.dl_model.load_state_dict(torch.load("models/ncf_model.pth", map_location=torch.device('cpu')))
            self.dl_model.eval()
            print("Backend: Deep Learning modeli yüklendi!")
        except Exception as e:
            print(f"Backend Uyarı: Model dosyası bulunamadı, klasik yöntemle devam ediliyor. Hata: {e}")

        print("Backend: Hibrit sistem hazır!")

    def get_popular(self):
        popular_ids = self.ratings.groupby('movieId').count()['rating'].sort_values(ascending=False).head(6).index.tolist()
        return self.movies[self.movies['movieId'].isin(popular_ids)][['movieId', 'title', 'genres']].to_dict(orient='records')

    def get_hybrid_rec(self, user_id, movie_id, top_n=6):
        """
        Hem Cosine Similarity (Klasik) hem de NCF (Deep Learning) skorlarını birleştirir.
        """
        # 1. Hata Kontrolü
        if movie_id not in self.similarity_df.columns:
            return self.get_popular()

        # 2. Klasik Skorlar (Cosine Similarity)
        similar_scores = self.similarity_df[movie_id].sort_values(ascending=False).iloc[1:50] # İlk 50 adayı al
        candidate_movie_ids = similar_scores.index.tolist()

        # 3. Deep Learning Skoru ile Yeniden Sıralama (Re-ranking)
        scored_candidates = []
        for cand_id in candidate_movie_ids:
            # Modelimize "Bu kullanıcı bu film için ne puan verir?" diye soruyoruz
            user_t = torch.LongTensor([user_id])
            item_t = torch.LongTensor([cand_id])
            
            with torch.no_grad():
                dl_score = self.dl_model(user_t, item_t).item()
            
            # Hibrit Skor Formülü:
            # Skor = (Klasik Benzerlik * 0.4) + (DL Tahmini * 0.6)
            classic_score = similar_scores[cand_id]
            hybrid_score = (classic_score * 0.4) + (dl_score * 0.6)
            
            scored_candidates.append((cand_id, hybrid_score))

        # 4. En yüksek skorlu olanları seç
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        final_ids = [x[0] for x in scored_candidates[:top_n]]

        return self.movies[self.movies['movieId'].isin(final_ids)][['movieId', 'title', 'genres']].to_dict(orient='records')