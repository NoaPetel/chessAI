import torch
import torch.nn as nn
import torch.nn.functional as F


class NNEval(nn.Module):

    def __init__(self, input_size=773, hidden_size=512, num_hidden_layers=3, dropout=0.2):
        super(NNEval, self).__init__()
        
        # Layers
        layers = []
        layers.append(nn.Linear(input_size, hidden_size))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(dropout))

        for _ in range(num_hidden_layers - 1):
            layers.append(nn.Linear(hidden_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))

        # Output: evaluation score (scalar)
        layers.append(nn.Linear(hidden_size, 1))
        self.model = nn.Sequential(*layers)

        
    def forward(self, x):
        return self.model(x)

    def train(self, train_loader, num_epochs=10):
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        for epoch in range(num_epochs):
            print("Epoch {epoch} ====================")
            for batch_x, batch_y in train_loader:
                optimizer.zero_grad()
                preds = self.model(batch_x)
                loss = criterion(preds, batch_y)
                loss.backward()
                optimizer.step()

    def save(self, path="nn_eval.pth"):
        torch.save(self.state_dict(), path)

    def load(self, path="nn_eval.pth"):
        self.load_state_dict(torch.load(path))
        
