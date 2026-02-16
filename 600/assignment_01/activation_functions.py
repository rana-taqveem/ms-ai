from abc import ABC, abstractmethod
import numpy as np

class ActivationFunction(ABC):

    @abstractmethod
    def forward(self, x: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def backward(self, gradient_last_layer: np.ndarray) -> np.ndarray:
        pass

class Relu(ActivationFunction):

    def __init__(self):
        super().__init__()
        self._forward_store: np.ndarray = np.array([])
        
    def forward(self, x: np.ndarray) -> np.ndarray:
        self._forward_store = np.maximum(0, x)
        return self._forward_store

    def backward(self, gradient_last_layer: np.ndarray) -> np.ndarray:
        return gradient_last_layer * np.where(self._forward_store > 0, 1, 0)
    
class Sigmoid(ActivationFunction):

    def __init__(self):
        super().__init__()
        self._forward_store: np.ndarray = np.array([])
        
    def forward(self, x: np.ndarray) -> np.ndarray:
        self._forward_store = 1 / (1 + np.exp(-x))
        return self._forward_store

    def backward(self, gradient_last_layer: np.ndarray) -> np.ndarray:
        return gradient_last_layer * self._forward_store * (1 - self._forward_store)
    
class Softmax(ActivationFunction):
    def __init__(self):
        super().__init__()
        print('Initializing Softmax activation function.')
        self._forward_store: np.ndarray = np.array([])
        
    def forward(self, x: np.ndarray) -> np.ndarray:
        x = x - np.max(x, axis=1, keepdims=True)
        e = np.exp(x)
        self._forward_store = e / np.sum(e, axis=1, keepdims=True)
        # print(f'forward store shape: {self._forward_store.shape}')
        # print(f'forward store: {self._forward_store}')
        return self._forward_store
    
    def backward(self, gradient_last_layer: np.ndarray) -> np.ndarray:
        
        # becasue a Softmax with cross entrpy loss has a gradient = y-y hast
        return gradient_last_layer
        # x = self._forward_store
        # # print(f'x shape: {x.shape}')
        # # print(f'gradient_last_layer shape: {gradient_last_layer.shape}')
        
        # if x.shape != gradient_last_layer.shape:
        #     raise ValueError(f'Shape mismatch: x shape {x.shape} and gradient_last_layer shape {gradient_last_layer.shape} must be the same.')
        
        
        # wavg_last_gradient = np.sum(x * gradient_last_layer, axis=1, keepdims=True)
        # return x * (gradient_last_layer - wavg_last_gradient)
        

    def backward_jacobian(self, gradient_last_layer: np.ndarray) -> np.ndarray:
        
        x = self._forward_store
        n, k = x.shape
        
        J = np.zeros((n, k, k))
        for i in range(n):
            xi = x[i].reshape(-1,1)
            xixj = np.dot(xi, xi.T)
            J[i] = np.diagflat(xi) - xixj
        
        gradient = np.einsum('ij,ijk->ik', gradient_last_layer, J)
        return gradient