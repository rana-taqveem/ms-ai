import numpy as np
from abc import ABC, abstractmethod

class LossFunction(ABC):
    
    @abstractmethod
    def compute_loss(self, y, y_hat):
        pass

    @abstractmethod
    def compute_gradient(self, y, y_hat) -> np.ndarray:
        pass
    
class CrossEntropyLoss(ABC):
    def __init__(self):
        self._loss = 0.0
    def compute_loss(self, y, y_hat):
        e = 1e-15
        y_hat = np.clip(y_hat, e, 1-e)
        self._loss = -np.sum(y * np.log(y_hat)) / y.shape[0]
        return self._loss
    
    def compute_gradient(self, y, y_hat):
        return y_hat - y
    
