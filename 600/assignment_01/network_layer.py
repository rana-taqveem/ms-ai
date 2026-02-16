import numpy as np
from activation_functions import ActivationFunction
class NetworkLayer:
    def __init__(self, w, b, num_of_neurons, activation_function:ActivationFunction):
        self.X = np.array([])
        self.w = w
        self.b = b
        self.d_w = np.array([])
        self.d_b = np.array([])
        self.num_of_neurons = num_of_neurons
        self.activation_function = activation_function
        
        self.grad_mean_store = []

    def forward(self, X):
        self.X = X
        self.a = np.dot(self.X, self.w) + self.b
        return self.activation_function.forward(self.a)
    
    def backward(self, gredient_last_layer: np.ndarray): 
        
        N = self.X.shape[0] 
        d_activation = self.activation_function.backward(gredient_last_layer)
        # print(f'd_activation shapre: {d_activation.shape}')
        
        self.d_w = np.dot(self.X.T, d_activation) / N
        # print(f'd_w shape: {self.d_w.shape}')
        
        self.d_b = np.sum(d_activation, axis=0, keepdims=True)/N
        # print(f'd_b shape: {self.d_b.shape}')
        
        self.grad_mean_store.append(np.mean(np.abs(self.d_w)))
        # print(f'Layers gradient mean: {self.grad_mean_store}')
 
        
        dX = np.dot(d_activation, self.w.T)
        return dX
    