import matplotlib.pyplot as plt
import torch 
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import PIL.Image as Image
from CNN import CNN

torch.random.manual_seed(0)

## Read an example image
I_PIL = Image.open('peppers.png')
I = transforms.ToTensor()(I_PIL)
# print(f"{I.shape}") # torch.Size([3, 384, 512])

## Create 12 linear filters
W = torch.randn((12, 3, 5, 5)) 


## Apply the filters to the images
Y = F.conv2d(I.unsqueeze_(0), W, bias=None, stride=1, padding=0)
# print(f"{Y.shape}") # torch.Size([1, 12, 380, 508]), on perd 2 lignes dans chaques directions car filtre 5x5

# Try again, downsampling the output (stride = 16)
Y_ds = F.conv2d(I, W, bias=None, stride=16, padding=0)



#%% Train loader
batch_size = 128
train_loader = torch.utils.data.DataLoader(dataset = training_set,
                                       batch_size=batch_size, #nombre d'éléments d'un minibatch
                                       shuffle=True, #mélanger la base de données à la fin de chaque epoch
                                       num_workers=2) #nombre de processus dédiées à la préparation des minibatches



#%% Valid loader
path_MNIST_valid = '/tmp/MNIST/Validation'                
valid_set = MNISTDataset(path_MNIST_valid)
valid_loader = torch.utils.data.DataLoader(dataset = valid_set,
                                       batch_size=batch_size,
                                       shuffle=False,#inutile de mélanger pour la validation
                                       num_workers=2)









# Instanciation d'un CNN sur GPU
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = CNN(10).to(device)

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

print('Number of parameters = {}'.format(count_parameters(model)))
































#%% Plots

## Visualize the input x
# fig1,ax1 = plt.subplots()
# ax1.imshow(I.permute((1,2,0))), plt.pause(0.1)
# print(f"{I.shape}") # torch.Size([3, 384, 512])

## Visualize the filters
# fig2,ax2 = plt.subplots()
# ax2.imshow(torchvision.utils.make_grid(W, padding=4, nrow=4, normalize=True, scale_each=True).permute(1,2,0))
# plt.show()

## Visualize the filtered images
# fig3,ax3 = plt.subplots()
# ax3.imshow(torchvision.utils.make_grid(Y.transpose(1,0), padding=4, nrow=4, normalize=True, scale_each=True).permute(1,2,0))
# plt.show()

## Visualize the downsampled filtered images
# fig4,ax4 = plt.subplots()
# ax4.imshow(torchvision.utils.make_grid(Y_ds.transpose(1,0), padding=0, nrow=4, normalize=True, scale_each=True).permute(1,2,0)) 
# plt.show

input("")