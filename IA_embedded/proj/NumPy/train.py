import matplotlib.pyplot as plt
import numpy as np
import sys

import utils
import functions
import MLP
import GradiantDescentWithMomentum as gdwm
import load_MNIST as MNIST

from functions import FC_backward, FC_forward, relu_backward, relu_forward, crossEntropyLoss


np.random.seed(0)


#%% MLP
def train(X, Y, C, H = 300, lr = 1e-2, beta = 0.9):
    N = X.shape[0]
    model = MLP.MLP(H, X.shape[1], C)
    optimizer = gdwm.GradientDescentWithMomentum(model, beta, lr)
    
    c_seq = []
    it_seq = []

    it = 0
    acc = 0
    c = 0
    while acc*100 < 90:    
        #Forward Pass
        X0,X1,X2,S = model.forward(X)
        
        #Compute Loss
        [c, dc_dS] = crossEntropyLoss(S, Y)
        
        #Print Loss and Classif Accuracy
        pred = np.argmax(S, axis=1)
        acc = (np.argmax(S, axis=1) == Y).astype('float').sum()/N
        #print('Iter {} | Training Loss = {} | Training Accuracy = {}%'.format(it,c,acc*100))

        #Backward Pass (Compute Gradient)
        optimizer.zero_grad()

        model.backward(dc_dS, S, X2, X1, X0)
        
        
        #Update Parameters
        optimizer.step()
        it += 1
        
        c_seq.append(c)
        it_seq.append(it)
    print('Iter {} | Training Loss = {} | Training Accuracy = {}%'.format(it,c,acc*100))


