from abc import ABC, abstractmethod
import numpy as np

class ActivationFunction(ABC):

    @abstractmethod
    def forward(self, x: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def backward(self, x: np.ndarray) -> np.ndarray:
        pass

class Relu(ActivationFunction):

    def __init__(self):
        super().__init__()
        self._forward_cache: np.ndarray = np.array([])
        
    def forward(self, x: np.ndarray) -> np.ndarray:
        self._forward_cache = np.maximum(0, x)
        return self._forward_cache

    def backward(self) -> np.ndarray:
        return np.where(self._forward_cache > 0, 1, 0)
    
class Sigmoid(ActivationFunction):

    def __init__(self):
        super().__init__()
        self._forward_cache: np.ndarray = np.array([])
        
    def forward(self, x: np.ndarray) -> np.ndarray:
        self._forward_cache = 1 / (1 + np.exp(-x))
        return self._forward_cache

    def backward(self) -> np.ndarray:
        return self._forward_cache * (1 - self._forward_cache)
    
class Softmax(ActivationFunction):
    def __init__(self):
        super().__init__()
        self._forward_cache: np.ndarray = np.array([])
        
    def forward(self, x: np.ndarray) -> np.ndarray:
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        self._forward_cache = exp_x / np.sum(exp_x, axis=1, keepdims=True)
        return self._forward_cache

    def backward(self) -> np.ndarray:
        s = self._forward_cache
        return s * (1 - s)