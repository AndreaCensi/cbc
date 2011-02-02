'''

We realized that it is not possible for us to release the entire source code 
(which includes unit tests, statistics, synthetic datasets, in the spirit of 
 reproducible research) at this time, because it would reveal our identity. 
In fact, it depends on several libraries we created which are easily Googlable.
 
As a temporary stand-in, we extracted the main routines and grouped them
in this file. At least, they should be able to clarify doubts from reading 
the pseudocode. Note that some steps are simplified.

'''

import numpy as np


def SSE(C, ndim):
    U, S, V = np.linalg.svd(C, full_matrices=0) 
    coords = V[:ndim, :]
    for i in range(ndim):
        coords[i, :] = coords[i, :]  * np.sqrt(S[i])
    N = coords.shape[1]
    for k in range(N):
        coords[:, k] = coords[:, k] / np.linalg.norm(coords[:, k])
    return coords
 
def SBSE(Y, ndim, a, iterations=10, nwarp=10, min_ratio=0.1):
    Y_order = order(Y)
    
    # The initial guess depends on the parameter a
    C0 = scale_linearly(Y_order, (a, 1)) 
    S = SSE(C0, ndim) 
    
    # Inner loop
    for i in range(iterations): # For simplicity, fixed iterations
        C = cosines_from_directions(S)
        C_sorted = np.sort(C.flat)
        Cp = C_sorted[Y_order]
        S = SSE(Cp, ndim)
    
    # Refinement stage (for simplicity, implemented here as a simple search)
    base_D = np.arccos(cosines_from_directions(S))
    diameter = base_D.max() 
    max_ratio = np.pi / diameter
    ratios = np.exp(np.linspace(np.log(min_ratio), np.log(max_ratio), nwarp))
    
    scores = []; guesses = []
    for ratio in ratios:
        Cwarp = np.cos(base_D * ratio)
        Sw = SSE(Cwarp, ndim)
        Cw_order = order(cosines_from_directions(Sw))
        score = correlation_coefficient(Cw_order, Y_order)
        
        scores.append(score)
        guesses.append(Sw)
    
    # choose best
    best = np.argmax(scores)
    S = guesses[best]
    score = scores[best]
    
    return S, score

def order(x):
    ''' order(x) is simply argsort(argsort(x)). '''
    # Return an array of the same shape
    order = np.zeros(dtype='int16', shape=x.shape)
    order.flat[:] = np.argsort(np.argsort(x.flat))
    return order

def cosines_from_directions(S):
    C = np.dot(S.T, S)
    return np.clip(C, -1, 1, C) # recover from numerical errors

def correlation_coefficient(x, y):
    ''' Returns the correlation between two sequences. '''
    correlation_matrix = np.corrcoef(x.flat, y.flat)
    assert correlation_matrix.shape == (2, 2)
    return np.clip(correlation_matrix[0, 1], -1.0, 1.0)
