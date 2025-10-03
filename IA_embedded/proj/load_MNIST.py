import PIL.Image as Image
from os import path
from os import listdir
import numpy as np
import math
import matplotlib.pyplot as plt

def load_MNIST(path_MNIST_bmp, mean_norm=0., std_norm=1.):
    
    filenames = listdir(path_MNIST_bmp)
    
    imgs_train = np.zeros((60000,28,28))
    labels_train = np.zeros(60000,dtype=np.uint8)
    n_train = 0
    
    imgs_test = np.zeros((10000,28,28))
    labels_test = np.zeros(10000,dtype=np.uint8)
    n_test = 0
    
    W=H=28
    for i, filename in enumerate(filenames):
        
        f_name, f_ext = path.splitext(filename)
        set_type, class_type ,num_im = f_name.split('_')
        
        num_im = int(num_im)
        img = np.array(Image.open(path.join(path_MNIST_bmp,filename)))/255.
        
        N_W = math.ceil(math.sqrt(num_im))
        N_H = math.ceil(num_im/N_W)
        
        im_array_ext = img.reshape(N_H,H,W*N_W).transpose((1,0,2))
        im_array_ext = im_array_ext.reshape(H,N_W*N_H,W).transpose((1,0,2))

        im_array = im_array_ext[:num_im,:,:]        
        
        if(set_type=='train'):
            imgs_train[n_train:n_train+num_im,:,:] = (im_array-mean_norm)/std_norm
            labels_train[n_train:n_train+num_im] = int(class_type)
            n_train += num_im
        elif(set_type=='test'):
            imgs_test[n_test:n_test+num_im,:,:] = (im_array-mean_norm)/std_norm
            labels_test[n_test:n_test+num_im] = int(class_type)
            n_test += num_im
                
    assert n_test == 10000
    assert n_train == 60000
        
        
    
    return imgs_train, labels_train, imgs_test, labels_test
    
if(__name__ == "__main__"):
    path_MNIST_bmp = './MNIST_bmp'

    imgs_train, labels_train, imgs_test, labels_test = load_MNIST(path_MNIST_bmp, mean_norm=0., std_norm=1.)
    n_train = imgs_train.shape[0]
    n_test = imgs_test.shape[0]
    
    ids = np.random.permutation(n_train)
    
    plt.figure()
    for i in range(8):
        for j in range(4):
            plt.subplot(4,8,i+1 + j*8)
            plt.imshow(imgs_train[ids[i+j*8],:,:])
            plt.title(labels_train[ids[i+j*8]])
            plt.axis('off')


    vec_train = imgs_train.reshape((n_train,-1))