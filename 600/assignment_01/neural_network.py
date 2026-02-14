import numpy as np
from activation_frunctions import ActivationFunction
from network_layer import NetworkLayer  
class NeuralNetwork:
    
    def __init__(self, input_dimension): 
        self.input_dimension = input_dimension
        self.layers = []
        self._forward_pass_res = np.array([])
        self._backward_pass_res= np.array([])
        self._cross_entropy_loss = 0.0
        
    def add_layer(self, num_of_neurons, activation_function:ActivationFunction):
        
        if len(self.layers) == 0:
            num_of_input_features = self.input_dimension
        else:
            num_of_input_features = self.layers[-1].num_of_neurons
            
        W = np.random.randn(num_of_input_features, num_of_neurons) * np.sqrt(2.0 / num_of_input_features)

        print(f'W shape: {W.shape}')
        b = np.zeros((1,num_of_neurons))
        print(f'b shape: {b.shape}')
        
        layer = NetworkLayer(w=W, b=b, activation_function=activation_function)
        self.layers.append(layer)
        
    def forward(self, X):
        for layer in self.layers:
            X = layer.forward(X)
            self._forward_pass_res = np.append(self._forward_pass_res, X)
        return X
    
    def cross_entropy_loss(self, y, y_hat):
        e = 1e-15
        y_hat = np.clip(y_hat, e, 1-e)
        self._cross_entropy_loss = -np.sum(y * np.log(y_hat)) / y.shape[0]
        return self._cross_entropy_loss
        
