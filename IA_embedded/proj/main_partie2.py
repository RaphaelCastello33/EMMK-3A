import matplotlib.pyplot as plt
import numpy as np
import sys

import utils
import functions
import MLP
import GradiantDescentWithMomentum as gdwm
from load_MNIST import load_MNIST
from train import train
from functions import FC_backward, FC_forward, relu_backward, relu_forward, crossEntropyLoss


path_MNIST_bmp = './MNIST_bmp'
imgs_train, labels_train, imgs_test, labels_test = load_MNIST(path_MNIST_bmp, mean_norm=0.1306, std_norm=0.3080)
n_train = imgs_train.shape[0]
n_test = imgs_test.shape[0]
ids = np.random.permutation(n_train)

#%% results before training
print("\nresults BEFORE training:")
plt.figure()
for i in range(8):
    for j in range(4):
        plt.subplot(4,8,i+1 + j*8)
        plt.imshow(imgs_train[ids[i+j*8],:,:])
        plt.title(labels_train[ids[i+j*8]])
        plt.axis('off')




vec_train = imgs_train.reshape((n_train,-1))

## Compute mean and std
mean = np.mean(imgs_train)
std = np.std(imgs_train)
print('Mean MNIST {}, Std MNIST {}'.format(mean, std))


#%% training MLP
print("\ntraining of the MLP...")

## vectorize the image
X = imgs_train.reshape(60000,28*28)
Y = labels_train
C = 10 # number of classes 

## train with the vectors
train(X, Y, C)

print("done !\n")

#%% results after training
print("\nresults AFTER training:")

plt.figure()
for i in range(8):
    for j in range(4):
        plt.subplot(4,8,i+1 + j*8)
        plt.imshow(X[ids[i+j*8],:,:])
        plt.title(Y[ids[i+j*8]])
        plt.axis('off')




vec_train = imgs_train.reshape((n_train,-1))

## Compute mean and std
mean = np.mean(imgs_train)
std = np.std(imgs_train)
print('Mean MNIST {}, Std MNIST {}'.format(mean, std))