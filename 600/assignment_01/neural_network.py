import numpy as np
from network_layer import NetworkLayer  
from loss_functions import LossFunction
from optimizers import Optimizer
from activation_functions import ActivationFunction
class NeuralNetwork:
    
    def __init__(self, input_dimension, loss_function:LossFunction, optimizer:Optimizer, weight_initializer=None): 
        self.input_dimension = input_dimension
        self.loss_function = loss_function
        self.optimizer = optimizer
        self.weight_initializer = weight_initializer
        
        self.layers: list[NetworkLayer] = []
        
    def add_layer(self, num_of_neurons, activation_function:ActivationFunction):
        
        if len(self.layers) == 0:
            num_of_input_features = self.input_dimension
        else:
            num_of_input_features = self.layers[-1].num_of_neurons
            
        if self.weight_initializer is not None:
            scaling_factor = self.weight_initializer(num_of_input_features)
            W = np.random.randn(num_of_input_features, num_of_neurons) * scaling_factor
        else:
            W = np.random.randn(num_of_input_features, num_of_neurons) * np.sqrt(2.0 / num_of_input_features)

        # print(f'W shape: {W.shape}')
        b = np.zeros((1,num_of_neurons))
        # print(f'b shape: {b.shape}')
        
        layer = NetworkLayer(w=W, b=b, num_of_neurons=num_of_neurons, activation_function=activation_function)
        self.layers.append(layer)
        
    def forward(self, X: np.ndarray):
        for layer in self.layers:
            X = layer.forward(X)
        return X

    def backward(self, y_hat, y):
        
        # to be changed to address if the loss function is not cross entropy loss
        # if self.loss_function == 'cross_entropy':
        #     delta_l = y_hat - y
        # else:
        #     delta_l = 2 * (y_hat - y) / y.shape[0] # just add a default case for now

        delta_l = self.loss_function.compute_gradient(y, y_hat)
        for layer in reversed(self.layers):
            delta_l = layer.backward(delta_l)
            
        
    def optimize(self):
        self.optimizer.take_step(self.layers)
        
    def evaluate(self, X, y):
        y_hat = self.forward(X)
        predictions = np.argmax(y_hat, axis=1)
        labels = np.argmax(y, axis=1)
        accuracy = np.mean(predictions == labels)
        return accuracy
        
    def compute_feature_importance(self, X, y, use_winning_class):
        y_hat = self.forward(X)
        
        if use_winning_class:
            # for winning classes as define in sec 2.8
            winning_class_indices = np.argmax(y_hat, axis=1)
            #print(winning_class_indices)
            delta_l = np.zeros_like(y_hat)
            delta_l[range(len(winning_class_indices)), winning_class_indices] = 1.0
            print(delta_l.shape)
        else:
            # if self.loss_function == 'cross_entropy':
            #     delta_l = y_hat - y
            # else:
            #     delta_l = 2 * (y_hat - y) / y.shape[0] # just add a default case for now
            delta_l = self.loss_function.compute_gradient(y, y_hat)
            for layer in reversed(self.layers):
                delta_l = layer.backward(delta_l)
                
        print(delta_l.shape)
                
        for layer in reversed(self.layers):
            delta_l = layer.backward(delta_l)
            
        print(delta_l.shape)
         
        g = np.mean(np.abs(delta_l), axis=0)
        dir = np.sign(-delta_l)
            
        ranked_features = np.argsort(g)[::-1]
        
        return ranked_features, g, dir
          
            
