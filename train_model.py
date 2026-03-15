import torch
import torch.optim as optim
import torch.nn as nn
import pandas as pd
from model_arch import NCFModel

# Veriyi yükle
ratings = pd.read_csv("data/ratings.csv")
num_users = ratings['userId'].max() + 1
num_items = ratings['movieId'].max() + 1

model = NCFModel(num_users, num_items)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

print("Eğitim başlıyor...")
# Basitleştirilmiş eğitim döngüsü
for epoch in range(5):
    users = torch.LongTensor(ratings['userId'].values)
    items = torch.LongTensor(ratings['movieId'].values)
    labels = torch.FloatTensor(ratings['rating'].values)
    
    optimizer.zero_grad()
    outputs = model(users, items).squeeze()
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1} tamamlandı. Loss: {loss.item():.4f}")

torch.save(model.state_dict(), "models/ncf_model.pth")
print("Model başarıyla kaydedildi!")