import torch
import torch.nn as nn

class NCFModel(nn.Module):
    def __init__(self, num_users, num_items, embedding_dim=32):
        super(NCFModel, self).__init__()
        self.user_embed = nn.Embedding(num_users, embedding_dim)
        self.item_embed = nn.Embedding(num_items, embedding_dim)
        
        # Basit bir Sinir Ağı Katmanı
        self.fc_layers = nn.Sequential(
            nn.Linear(embedding_dim * 2, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1) # Rating tahmini (Örn: 0-5 arası)
        )

    def forward(self, user_indices, item_indices):
        u_emb = self.user_embed(user_indices)
        i_emb = self.item_embed(item_indices)
        x = torch.cat([u_emb, i_emb], dim=-1)
        return self.fc_layers(x)