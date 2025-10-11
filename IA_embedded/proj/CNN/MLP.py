from functions import FC_backward, FC_forward, relu_backward, relu_forward
import numpy as np
import torch
class MLP:
    def __init__(self, H, D, C):


        self.H = H
        self.D = D
        self.C = C
        

        # Initialisation des poids et des biais avec PyTorch
        self.W1 = (torch.sqrt(torch.tensor(6. / D)) * (2 * (torch.rand(D, H) - 0.5))).float()
        self.b1 = (1. / torch.sqrt(torch.tensor(D, dtype=torch.float))) * (2 * (torch.rand(H) - 0.5)).float()
        self.W3 = (torch.sqrt(torch.tensor(6. / H, dtype=torch.float)) * (2 * (torch.rand(H, C) - 0.5))).float()
        self.b3 = (1. / torch.sqrt(torch.tensor(H, dtype=torch.float))) * (2 * (torch.rand(C) - 0.5)).float()
        
        # Initialisation des gradients avec PyTorch
        self.dc_dW1 = torch.zeros_like(self.W1)
        self.dc_db1 = torch.zeros_like(self.b1)
        self.dc_dW3 = torch.zeros_like(self.W3)
        self.dc_db3 = torch.zeros_like(self.b3)
        

        
    def forward(self,X):
    
        X1 = FC_forward(X, self.W1, self.b1) #NxH
        X2 = relu_forward(X1) #NxH
        S = FC_forward(X2, self.W3, self.b3) #NxC
    
        return X,X1,X2,S
    
    def backward(self,dc_dS, S, X2, X1, X0):
        
        dc_dX2, dc_dW3, dc_db3 = FC_backward(dc_dS, X2, self.W3, self.b3)
        self.dc_dW3 += dc_dW3
        self.dc_db3 += dc_db3
        
        dc_dX1 = relu_backward(dc_dX2, X1)
        
        dc_dX0, dc_dW1, dc_db1 = FC_backward(dc_dX1, X0, self.W1, self.b1)
        self.dc_dW1 += dc_dW1
        self.dc_db1 += dc_db1
        
        
        return