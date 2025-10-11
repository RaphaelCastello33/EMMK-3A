import torch
from MNISTDataset import MNISTDataset
import torchvision.transforms as T
import matplotlib.pyplot as plt
import torch.nn as nn
from train import train

torch.random.manual_seed(0)
path_MNIST_train = './MNIST/Training'
mean_norm = 0.1306
std_norm = 0.3081            
training_set = MNISTDataset(path_MNIST_train, mean_norm=mean_norm, std_norm=std_norm)

#%% Show 4 pairs of data
fig1, axs1 = plt.subplots(ncols=4)

offset = 7000
for i in range(4):
    image, label, _ = training_set[i+offset]
    axs1[i].imshow(T.ToPILImage()((image*std_norm)+mean_norm))
    axs1[i].set_title('True label {}'.format(label))
    
plt.pause(1.)


#%% Compute mean and std
# mean = 0
# data_full = []
# for i in range(len(training_set)):
#     if(i%10000==0):
#         print(i)
#     image, label, _ = training_set[i]
#     data_full.append(image.ravel().data) #stores all data, only possible because MNIST is small
    

# data_full_concat = torch.cat(data_full)
# mean = torch.mean(data_full_concat)
# std = torch.std(data_full_concat)
# print('Mean MNIST {}, Std MNIST {}'.format(mean, std)) # mean_norm=0.1306, std_norm=0.3080

batch_size = 128
train_loader = torch.utils.data.DataLoader(dataset = training_set,
                                       batch_size=batch_size, #nombre d'éléments d'un minibatch
                                       shuffle=True, #mélanger la base de données à la fin de chaque epoch
                                       num_workers=2) #nombre de processus dédiées à la préparation des minibatches
images, labels, _ = next(iter(train_loader))

#%% Show 10 pairs of data
fig2, axs2 = plt.subplots(ncols=10)
for i in range(10):
    axs2[i].imshow(T.ToPILImage()((images[i,:,:,:]*std_norm)+mean_norm))
    axs2[i].set_title('{}'.format(labels[i]))
    
plt.pause(1.)

print(f"image.shape = {images.shape}") # image.shape = 128x1x28x28 (taille minibatche = 128, 1 canal, image de 28x28 )
print(f"labels.shape = {labels.shape}") # image.shape = 128 (128 etiquettes)


path_MNIST_valid = './MNIST/Validation'                
valid_set = MNISTDataset(path_MNIST_valid)
valid_loader = torch.utils.data.DataLoader(dataset = valid_set,
                                       batch_size=batch_size,
                                       shuffle=False,#inutile de mélanger pour la validation
                                       num_workers=2)

# Show 10 pairs of data
images, labels, _ = next(iter(valid_loader))
fig3, axs3 = plt.subplots(ncols=10)
for i in range(10):
    axs3[i].imshow(T.ToPILImage()((images[i,:,:,:]*std_norm)+mean_norm))
    axs3[i].set_title('{}'.format(labels[i]))
    
plt.pause(1.)


print(f"dataloader.shape = {images.view(-1, 28*28).shape}")
# train(training_set.img_list.view(-1, 784), training_set.label_list, training_set.num_classes )
#print(f"{images.view(-1, 28*28).shape[0]}, {images.view(-1, 28*28).shape[1]}") # {128, 784}

train(images, labels)

input("")