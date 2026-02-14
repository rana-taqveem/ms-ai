import numpy as np
from activation_frunctions import ActivationFunction
from network_layer import NetworkLayer  
class NeuralNetwork:
    
    def __init__(self, input_dimension): 
        self.input_dimension = input_dimension
        self.layers = []
        
    def add_layer(self, num_of_neurons, activation_function:ActivationFunction):
        
        if len(self.layers) == 0:
            num_of_input_features = self.input_dimension
        else:
            num_of_input_features = self.layers[-1].num_of_neurons
            
        W = np.random.randn(num_of_input_features, num_of_neurons) * np.sqrt(2.0 / num_of_input_features)
        b = np.zeros((1,num_of_neurons))
        layer = NetworkLayer(w=W, b=b, activation_function=activation_function)
        self.layers.append(layer)
        
    def forward(self, X):
        for layer in self.layers:
            X = layer.forward(X)
        return X