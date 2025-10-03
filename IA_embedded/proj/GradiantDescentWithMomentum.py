import numpy as np

class GradientDescentWithMomentum:
    def __init__(self, model, beta, lr):
        
        self.model = model
        self.beta= beta
        self.lr = lr
        
        #momentum
        self.VW1 = np.zeros_like(self.model.W1)
        self.Vb1 = np.zeros_like(self.model.b1)
        self.VW3 = np.zeros_like(self.model.W3)
        self.Vb3 = np.zeros_like(self.model.b3)
        
        self.is_init = True
    def step(self):
        if(self.is_init == True):
            self.VW1 = self.model.dc_dW1      
            self.VW3 = self.model.dc_dW3         
            self.Vb1 = self.model.dc_db1           
            self.Vb3 = self.model.dc_db3
            self.is_init = False
        else:            
            self.VW1 = self.beta*self.VW1 + self.model.dc_dW1
            self.VW3 = self.beta*self.VW3 + self.model.dc_dW3
            self.Vb1 = self.beta*self.Vb1 + self.model.dc_db1
            self.Vb3 = self.beta*self.Vb3 + self.model.dc_db3
        
        self.model.W1 -= self.lr*self.VW1
        self.model.W3 -= self.lr*self.VW3
        self.model.b1 -= self.lr*self.Vb1
        self.model.b3 -= self.lr*self.Vb3
    
    def zero_grad(self):
        self.model.dc_dW1.fill(0.)
        self.model.dc_db1.fill(0.)
        self.model.dc_dW3.fill(0.)
        self.model.dc_db3.fill(0.)