import numpy as np
import matplotlib.pyplot as plt
import torch 

def FC_forward(X, W, b):
    Z = X @ W + b  # NxH
    return Z

def FC_backward(dc_dZ, X, W, b):
    # S'assurer que tous les tenseurs sont du même type (float32)
    dc_dZ = dc_dZ.to(torch.float32)
    W = W.to(torch.float32)
    
    dc_dX = dc_dZ @ W.T
    dc_dW = X.T @ dc_dZ
    dc_db = dc_dZ.sum(dim=0)
    return dc_dX, dc_dW, dc_db

def relu_forward(X):
    Z = torch.relu(X) 
    return Z

def relu_backward(dc_dZ, X):
    dc_dX = torch.where(X > 0, dc_dZ, torch.zeros_like(dc_dZ)) 
    return dc_dX

def logsoftmax(x):
    x_shift = x - torch.max(x, dim=1, keepdim=True).values  # Remplacer np.amax par torch.max
    return x_shift - torch.log(torch.exp(x_shift).sum(dim=1, keepdim=True))  # Remplacer np.exp et np.log

def softmax(x):
    e_x = torch.exp(x - torch.max(x, dim=1, keepdim=True).values)  # Remplacer np.exp et np.amax
    return e_x / e_x.sum(dim=1, keepdim=True)  # Remplacer np.sum
    
def crossEntropyLoss(S, y):
    N = y.shape[0]
    # Assurez-vous que S et y sont du même type (float32 ici)
    S = S.to(torch.float32)  # Convertir S en float32
    y = y.to(torch.int64)  # Assurez-vous que y est en int64 pour l'indexation
    
    P = softmax(S)
    log_p = logsoftmax(S)
    
    a = log_p[torch.arange(N), y]
    l = -a.sum() / N
    
    # Calcul du gradient
    dc_dS = P
    dc_dS[torch.arange(N), y] -= 1
    dc_dS = dc_dS / N
    
    return l, dc_dS
