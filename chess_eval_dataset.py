from utils import fen_to_tensor
import torch
from torch.utils.data import DataLoader, Dataset

class ChessEvalDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        fen, eval_score = self.data[idx]
        x = fen_to_tensor(fen)  # 773-dimensional tensor
        y = torch.tensor([eval_score], dtype=torch.float32)
        return x, y
