import numpy as np
from activation_functions import ActivationFunction
class NetworkLayer:
    def __init__(self, w, b, num_of_neurons, activation_function:ActivationFunction):
        self.X = np.array([])
        self.w = w
        self.b = b
        self.dw = np.array([])
        self.db = np.array([])
        self.num_of_neurons = num_of_neurons
        self.activation_function = activation_function

    def forward(self, X):
        self.X = X
        self.a = np.dot(self.X, self.w) + self.b
        return self.activation_function.forward(self.a)
    
    def backward(self, gredient_last_layer: np.ndarray):  
        d_activation = self.activation_function.backward(gredient_last_layer)
        self.dw = np.dot(self.X.T, d_activation)
        self.db = np.sum(d_activation, axis=0, keepdims=True)
        dX = np.dot(d_activation, self.w.T)
        return dX