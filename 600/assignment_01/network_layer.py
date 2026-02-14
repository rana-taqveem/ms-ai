import numpy as np
from activation_frunctions import ActivationFunction
class NetworkLayer:
    def __init__(self, w, b, activation_function:ActivationFunction):
        self.X = np.array([])
        self.w = w
        self.b = b
        self.num_of_neurons = self.w.shape[1]
        self.activation_function = activation_function
        self._pre_activation_results: np.ndarray = np.array([])
        self._post_activation_results: np.ndarray = np.array([])

    def forward(self, X):
        self.X = X
        self._pre_activation_results = np.dot(self.X, self.w) + self.b
        print(f'pre activation results: {self._pre_activation_results}')
        print(f'pre activation results shape: {self._pre_activation_results.shape}')
        self._post_activation_results = self.activation_function.forward(self._pre_activation_results) 
        print(f'post activation results: {self._post_activation_results}')
        print(f'post activation results shape: {self._post_activation_results.shape}')       
        
        return self._post_activation_results
    
    def get_post_activation_results(self):
        return self._post_activation_results
    
    def get_pre_activation_results(self):
        return self._pre_activation_results