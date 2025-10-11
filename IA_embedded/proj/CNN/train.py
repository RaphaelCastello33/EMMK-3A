import matplotlib.pyplot as plt
import numpy as np
import sys
import torch
import utils
import functions
import MLP
import GradiantDescentWithMomentum as gdwm

from functions import FC_backward, FC_forward, relu_backward, relu_forward, crossEntropyLoss


np.random.seed(0)


#%% MLP
def train(X, Y, C=10, H = 300, lr = 1e-2, beta = 0.9):
    N = X.shape[0] # 128
    model = MLP.MLP(H, X.view(-1, 28*28).shape[1], C)
    optimizer = gdwm.GradientDescentWithMomentum(model, beta, lr)
    
    c_seq = []
    it_seq = []

    it = 0
    acc = 0
    c = 0
    while acc*100 != 100:    
        #Forward Pass
        X0,X1,X2,S = model.forward(X.view(-1, 28*28))
        
        #Compute Loss
        [c, dc_dS] = crossEntropyLoss(S, Y)
        
        #Print Loss and Classif Accuracy
        acc = (torch.argmax(S, dim=1) == Y).float().sum() / N  # Remplacer np.argmax et .astype('float')        print('Iter {} | Training Loss = {} | Training Accuracy = {}%'.format(it,c,acc*100))

        #Backward Pass (Compute Gradient)
        optimizer.zero_grad()

        model.backward(dc_dS, S, X2, X1, X0)
        print('Iter {} | Training Loss = {} | Training Accuracy = {}%'.format(it,c,acc*100))

        
        #Update Parameters
        optimizer.step()
        it += 1
        
        c_seq.append(c)
        it_seq.append(it)


