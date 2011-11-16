import numpy as np
from cbc.tools import distances_from_directions

def y_corr(Y, true_S):
    R = np.corrcoef(Y, rowvar=0)
    return R.astype('float32')

def y_dot_corr(Y, true_S):
    y0 = Y[:-1, :].astype('float32')
    y1 = Y[+1:, :].astype('float32')
    Y = y1 - y0
    R = np.corrcoef(Y, rowvar=0)
    return R.astype('float32')

def y_dot_sign_corr(Y, true_S):
    y0 = Y[:-1, :].astype('float32')
    y1 = Y[+1:, :].astype('float32')
    Y = y1 - y0
    Y = np.sign(Y)
    R = np.corrcoef(Y, rowvar=0)
    return R.astype('float32')
    
def artificial(Y, true_S):
    if true_S is None:
        return true_S
        
    print('Computing correlation')
    true_D = distances_from_directions(true_S)
    def exponential_kernel(D, alpha):
        return np.exp(-D / alpha)
    R = exponential_kernel(true_D, alpha=0.52) 
    
    return R.astype('float32')
