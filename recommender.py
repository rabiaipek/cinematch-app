import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MovieEngine:
    def __init__(self):
        print("Backend: Model ve veriler yukleniyor...")
        self.movies = pd.read_csv("data/movies.csv")
        self.ratings = pd.read_csv("data/ratings.csv")
        
        # 1. Veri Ön İşleme (Sadece yeterli oy alan kullanıcıları/filmleri tutalım)
        # En az 20 film oylayan kullanıcıları tut
        user_counts = self.ratings['userId'].value_counts()
        active_users = user_counts[user_counts >= 20].index
        self.ratings = self.ratings[self.ratings['userId'].isin(active_users)]
        
        # En az 5 oy alan filmleri tut
        movie_counts = self.ratings['movieId'].value_counts()
        popular_movies = movie_counts[movie_counts >= 5].index
        self.ratings = self.ratings[self.ratings['movieId'].isin(popular_movies)]
        
        # 2. Matris Oluşturma (Kullanıcı-Film Matrisi)
        user_movie_matrix = self.ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
        
        # 3. Kosinüs Benzerliği Hesaplama (Filmler Arası)
        # Sütun bazlı (filmler arası) benzerlik hesaplıyoruz
        item_similarity = cosine_similarity(user_movie_matrix.T)
        self.similarity_df = pd.DataFrame(item_similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)
        
        print("Backend: Model ve veriler hazir!")

    def get_popular(self):
        # En popüler 6 filmi (oy sayısına göre) getir
        popular_ids = self.ratings.groupby('movieId').count()['rating'].sort_values(ascending=False).head(6).index.tolist()
        return self.movies[self.movies['movieId'].isin(popular_ids)][['title', 'genres']].to_dict(orient='records')

    def get_rec(self, movie_id):
        # 4. Hata Kontrolü (Cold Start)
        if movie_id not in self.similarity_df.columns:
            return self.get_popular()
        
        # 5. Benzer Filmleri Bulma
        # Kendisi hariç (iloc[1:]) en benzer 6 filmi al
        similar_ids = self.similarity_df[movie_id].sort_values(ascending=False).iloc[1:7].index.tolist()
        
        # 6. Detaylı Bilgi Döndürme
        return self.movies[self.movies['movieId'].isin(similar_ids)][['title', 'genres']].to_dict(orient='records')