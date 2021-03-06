import torch
import torch.nn as nn
import torch.nn.functional as F
from modules.cbhg import CBHG
from modules.prenet import PreNet
import sys


class Encoder(nn.Module):

    def __init__(self, num_embeddings, embedding_dim,
                 bank_k, bank_ck, proj_dims, highway_layers,
                 highway_units, gru_units,
                 dropout=0.5, use_cuda=False):
        super(Encoder, self).__init__()
        self.embedding = nn.Embedding(num_embeddings, embedding_dim)
        self.prenet = PreNet(embedding_dim, dropout=dropout)
        self.cbhg = CBHG(
            self.prenet.fc2_hidden_size, bank_k, bank_ck,
            proj_dims, highway_layers, highway_units,
            gru_units, use_cuda=use_cuda
        )

    def forward(self, x):
        """
        Args:
            x: A Tensor of size (batch_size, time_steps)

        Returns:
            A Tensor of size (batch_size, time_steps, 2 * gru_units)
        """
        embedded = self.embedding(x)
        return self.cbhg(self.prenet(embedded))
