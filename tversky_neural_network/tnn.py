from __future__ import annotations
from torch.nn import Module

class TverskyProjectionLayer(Module):
    
    def __init__(self):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        return x

class TverskySimilarityLayer(Module):
    
    def __init__(self):
        super().__init__()
        raise NotImplementedError
    
    def forward(self, x):
        return x
