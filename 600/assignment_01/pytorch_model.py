import torch
import torch.nn as nn


class PytorchModel(nn.Module):
    def __init__(self, input_dimension, hidden_dimension, output_dimension, activation_function):
        super(PytorchModel, self).__init__()
        self.HL1 = nn.Linear(input_dimension, hidden_dimension)
        self.HL1 = nn.Linear(hidden_dimension, hidden_dimension)
        self.output = nn.Linear(input_dimension, output_dimension)
        self.activation_function = activation_function
        
    def forward(self, X):
        X1 = self.activation_function(self.HL1(X))
        X2 = self.activation_function(self.HL2(X1))
        X3 = self.output(X2)
        
        return X3
    
        