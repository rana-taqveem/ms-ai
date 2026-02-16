from network_layer import NetworkLayer
from abc import ABC, abstractmethod
class Optimizer(ABC):

    @abstractmethod
    def take_step(self, layers: list[NetworkLayer]):
        pass

class GradientDescent(Optimizer):
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate
    
    def take_step(self, layers: list[NetworkLayer]):
        for layer in layers:
            layer.w -= self.learning_rate * layer.d_w
            layer.b -= self.learning_rate * layer.d_b
            
            
# class BatchGradientDescent(Optimizer):
#     def __init__(self, learning_rate=0.01, batch_size=32):
#         self.learning_rate = learning_rate
#         self.batch_size = batch_size
    
#     def take_step(self, layers: list[NetworkLayer]):
#         for layer in layers:
#             layer.w -= self.learning_rate * layer.d_w
#             layer.b -= self.learning_rate * layer.d_b