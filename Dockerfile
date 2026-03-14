# 1. Temel imaj İçinde Python 3.9 olan hafif bir Linux sürümü kullanıyoruz
FROM python:3.9-slim

# 2. Çalışma klasörü Konteyner içinde kodların duracağı yeri belirliyoruz
WORKDIR app

# 3. Kütüphane listesini konteyner içine kopyalıyoruz
COPY requirements.txt .

# 4. Kütüphaneleri yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tüm proje dosyalarını (kodlar, csv vb.) konteyner içine kopyalıyoruz
COPY . .

# 6. Uygulamanın çalışacağı portu dış dünyaya açıyoruz (Streamlit varsayılan 8501)
EXPOSE 8501

# 7. Konteyner başladığında çalışacak komut
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]