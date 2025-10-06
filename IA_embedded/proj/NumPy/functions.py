import numpy as np
import matplotlib.pyplot as plt

def FC_forward(X,W,b):
    Z = X.dot(W) + b #NxH
    return Z

def FC_backward(dc_dZ, X, W, b):
    dc_dX = dc_dZ@(W.T)
    dc_dW = X.T@(dc_dZ)
    dc_db = np.sum(dc_dZ, axis=0)
    return dc_dX, dc_dW, dc_db

def relu_forward(X):
    Z = np.maximum(0.,X) 
    return Z

def relu_backward(dc_dZ, X):
    dc_dX = np.where(X > 0, dc_dZ, 0.0)
    return dc_dX

def logsoftmax(x):
    x_shift = x - np.amax(x, axis=1, keepdims=True)
    return x_shift - np.log(np.exp(x_shift).sum(axis=1, keepdims=True))   
    
def softmax(x):
    e_x = np.exp(x - np.amax(x, axis=1, keepdims=True))
    return e_x / e_x.sum(axis=1, keepdims=True)
    
def crossEntropyLoss(S, y):
    N = y.shape[0]
    P = softmax(S.astype('double'))
    log_p = logsoftmax(S.astype('double'))
    a = log_p[np.arange(N),y]
    l = -a.sum()/N
    dc_dS = P
    dc_dS[np.arange(N),y] -= 1
    dc_dS = dc_dS/N
    return (l, dc_dS)