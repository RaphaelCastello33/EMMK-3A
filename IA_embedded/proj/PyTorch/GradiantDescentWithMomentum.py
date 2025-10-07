import torch

class GradientDescentWithMomentum:
    def __init__(self, model, beta, lr):
        self.model = model
        self.beta = beta
        self.lr = lr
        
        # Initialisation des variables de momentum avec des tenseurs PyTorch
        self.VW1 = torch.zeros_like(self.model.W1)
        self.Vb1 = torch.zeros_like(self.model.b1)
        self.VW3 = torch.zeros_like(self.model.W3)
        self.Vb3 = torch.zeros_like(self.model.b3)
        
        self.is_init = True
        
    def step(self):
        if self.is_init:
            self.VW1 = self.model.dc_dW1      
            self.VW3 = self.model.dc_dW3         
            self.Vb1 = self.model.dc_db1           
            self.Vb3 = self.model.dc_db3
            self.is_init = False
        else:
            # Mise à jour avec momentum
            self.VW1 = self.beta * self.VW1 + self.model.dc_dW1
            self.VW3 = self.beta * self.VW3 + self.model.dc_dW3
            self.Vb1 = self.beta * self.Vb1 + self.model.dc_db1
            self.Vb3 = self.beta * self.Vb3 + self.model.dc_db3
        
        # Mise à jour des poids avec les gradients et le momentum
        self.model.W1 -= self.lr * self.VW1
        self.model.W3 -= self.lr * self.VW3
        self.model.b1 -= self.lr * self.Vb1
        self.model.b3 -= self.lr * self.Vb3
    
    def zero_grad(self):
        # Mise à zéro des gradients avec la méthode fill_() pour les tenseurs PyTorch
        self.model.dc_dW1.fill_(0.)
        self.model.dc_db1.fill_(0.)
        self.model.dc_dW3.fill_(0.)
        self.model.dc_db3.fill_(0.)
