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

#%% DEFINE AND PLOT DATA
    
style_per_class = ['xb', 'or', 'sg']
X = np.array([[1.2, 2.3, -0.7, 3.2, -1.3],[-3.4, 2.8, 1.2, -0.4, -2.3]]).T
X -= X.mean() #centering data (globally)
X /= X.std() #reduce data (globally)
y = np.array([0,0,1,1,2])

C = len(style_per_class)
N = X.shape[0]
xx, yy = utils.make_meshgrid(X[:,0], X[:,1], h=0.05)


fig1, axs1 = plt.subplots(ncols=2)
axs1[0].set_xlim(xx.min(), xx.max())
axs1[0].set_ylim(yy.min(), yy.max())
axs1[0].grid(True)

for i in range(C):
    x_c = X[y==i,:]
    axs1[0].plot(x_c[:,0],x_c[:,1],style_per_class[i],markersize=7, markeredgewidth=3.)

plt.pause(0.1)
# plt.show() 


#%% calcul du gradiant


utils.test_FC_backward()
utils.test_relu_backward()


#%% MLP

# HYPERPARAMETERS
H = 300
lr = 1e-2 #learning rate
beta = 0.9 #momentum parameter

model = MLP.MLP(H)
optimizer = gdwm.GradientDescentWithMomentum(model, beta, lr)

c_seq = []
it_seq = []
line_loss, = axs1[1].plot(it_seq,c_seq)
axs1[1].legend()
axs1[1].set_xlabel('Iterations')

it = 0
while 1:    
    #Forward Pass
    X0,X1,X2,S = model.forward(X)
    
    #Compute Loss
    [c, dc_dS] = crossEntropyLoss(S, y)
    
    #Print Loss and Classif Accuracy
    pred = np.argmax(S, axis=1)
    acc = (np.argmax(S, axis=1) == y).astype('float').sum()/N
    print('Iter {} | Training Loss = {} | Training Accuracy = {}%'.format(it,c,acc*100))

    #Backward Pass (Compute Gradient)
    optimizer.zero_grad()

    model.backward(dc_dS, S, X2, X1, X0)
    
    
    #Update Parameters
    optimizer.step()
    it += 1
    
    c_seq.append(c)
    it_seq.append(it)
    if(np.mod(it,10)==0):
        #Plot decision boundary
        axs1[0].cla()
        
        for i in range(C):
            x_c = X[y==i,:]
            axs1[0].plot(x_c[:,0],x_c[:,1],style_per_class[i],markersize=7, markeredgewidth=3.)
        utils.plot_contours(axs1[0], model, xx, yy, cmap=plt.cm.coolwarm, alpha=0.8)
        
        
        line_loss.remove()
        
        line_loss, = axs1[1].plot(it_seq,c_seq,'r',label='Training loss')
        axs1[1].legend()
        fig1.canvas.draw()
        fig1.canvas.flush_events()
        plt.pause(0.1)
        plt.ion()
        plt.show()


