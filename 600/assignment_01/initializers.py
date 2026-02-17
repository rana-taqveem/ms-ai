import numpy as np

class WeightInitializer:

    @staticmethod
    def xavier_glorot(num_of_input_features):
        return np.sqrt(1.0 / num_of_input_features)
    
    @staticmethod
    def he_kaiming(num_of_input_features):
        return np.sqrt(2.0 / num_of_input_features)