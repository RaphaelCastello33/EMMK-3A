import numpy as np
from functions import FC_backward, FC_forward, relu_backward, relu_forward
import sys

def plot_contours(ax, model, xx, yy, **params):
    """Plot the decision boundaries for a classifier.
    Parameters
    ----------
    ax: matplotlib axes object
    W: weight matrix
    b: bias vector
    xx: meshgrid ndarray
    yy: meshgrid ndarray
    params: dictionary of params to pass to contourf, optional
    """
    _,_,_,S = model.forward(np.c_[xx.ravel(), yy.ravel()])
    pred = np.argmax(S, axis=1)
    Z = pred.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    
    return out

def make_meshgrid(x, y, h=.02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),np.arange(y_min, y_max, h))
    return xx, yy


def test_FC_backward():
    
    eta = 1e-5
    N = 100
    D = 10
    H = 20
    X = np.random.normal(size=(N,D))
    dX = np.random.normal(size=(N,D))
    W = np.random.normal(size=(D,H))
    b = np.random.normal(size=(H))
    dW = np.random.normal(size=(D,H))
    db = np.random.normal(size=(H))


    ddX_approx = (FC_forward(X+eta*dX,W,b).sum() - FC_forward(X,W,b).sum())/eta
    dc_dX, _, _ = FC_backward(np.ones((N,H)), X, W, b)
    ddX = (dc_dX*dX).sum()
    if(np.isclose(ddX,ddX_approx)):
        print('Test FC_backward dl_dX: SUCCESS')
    else:
        print('Test FC_backward dl_dX: FAILURE')
        sys.exit()
    
    ddW_approx = (FC_forward(X,W+eta*dW,b).sum() - FC_forward(X,W,b).sum())/eta
    _, dc_dW, _ = FC_backward(np.ones((N,H)), X, W, b)
    ddW = (dc_dW*dW).sum()
    if(np.isclose(ddW,ddW_approx)):
        print('Test FC_backward dl_dW: SUCCESS')
    else:
        print('Test FC_backward dl_dW: FAILURE')
        sys.exit()
    
    ddb_approx = (FC_forward(X,W,b+eta*db).sum() - FC_forward(X,W,b).sum())/eta
    _, _, dc_db = FC_backward(np.ones((N,H)), X, W, b)
    ddb = (dc_db*db).sum()
    if(np.isclose(ddb,ddb_approx)):
        print('Test FC_backward dl_db: SUCCESS')
    else:
        print('Test FC_backward dl_db: FAILURE')
        sys.exit()
    
    return



def test_relu_backward():
    
    eta = 1e-5
    N = 100
    D = 10
    X = np.random.normal(size=(N,D))
    dX = np.random.normal(size=(N,D))

    ddX_approx = (relu_forward(X+eta*dX).sum() - relu_forward(X).sum())/eta
    dc_dX = relu_backward(np.ones((N,D)), X)
    ddX = (dc_dX*dX).sum()
    if(np.isclose(ddX,ddX_approx)):
        print('Test relu_backward dl_db: SUCCESS')
    else:
        print('Test relu_backward dl_db: FAILURE')
        sys.exit()
    
    return