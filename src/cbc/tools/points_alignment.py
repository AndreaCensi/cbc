import numpy as np
from contracts import contracts, check, new_contract
from snp_geometry import assert_allclose, geodesic_distance_on_sphere
import time

@new_contract
@contracts(X='array[KxN],K>0,N>0')
def directions(X):
    ''' Checks that every column has unit length. '''
    K = X.shape[1]
    for i in range(K):
        v = X[:, i]
        assert_allclose(1, np.linalg.norm(v) , rtol=1e-5)

@contracts(X='array[KxN],K>=2', Y='array[KxN]', returns='array[KxK],orthogonal')
def find_best_orthogonal_transform(X, Y):
    ''' Finds the best orthogonal transform R (R in O(K)) between X and Y,
        such that R X ~= Y. '''
    YX = np.dot(Y, X.T)
    check('array[KxK]', YX)
    
    U, S, V = np.linalg.svd(YX) #@UnusedVariable
    
    best = np.dot(U, V)
    return best
    
@contracts(X='array[KxN],(K=2|K=3)', Y='array[KxN]', returns='float,>=0')
def overlap_error_after_orthogonal_transform(X, Y):
    ''' Computes the norm of the residual after X and Y (vectors of direction)
        are optimally rotated/mirrored to best overlap with each other. 
        The result is returned in average degrees.
    '''
    O = find_best_orthogonal_transform(X, Y)
    X2 = np.dot(O, X)
    return average_geodesic_error(X2, Y)

# TODO: add unit test for these
@contracts(X='directions,array[KxN]', Y='directions,array[KxN]',)
def average_geodesic_error(X, Y):
    return np.arccos(np.clip((X * Y).sum(axis=0), -1, +1)).mean()
#    N = X.shape[1]
#    total_error = 0
#    for i in range(N):
#        x, y = X[:, i], Y[:, i]
#        total_error += geodesic_distance_on_sphere(x, y) 
#    return total_error / N 
    
    
