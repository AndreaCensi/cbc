from contracts import contracts, check_multiple
import numpy as np


def create_histogram_2d(x, y, resolution):
    edges = np.linspace(-1, 1, resolution)
    H, xe, ye = np.histogram2d(x.flatten(), y.flatten(), bins=(edges, edges)) #@UnusedVariable
    return H

def create_s_from_theta(theta):
    return np.vstack((np.cos(theta), np.sin(theta), 0 * theta))


@contracts(S='array[KxN],K<N', returns='array[NxN]')
def get_cosine_matrix_from_s(S):
    C = np.dot(S.T, S)
    return np.clip(C, -1, 1, C)

@contracts(C='array[NxN](>=-1,<=1)', returns='array[NxN]')
def get_distance_matrix_from_cosine(C):
    return np.real(np.arccos(C))


@contracts(R='array[NxN]', ndim='int,K', returns='array[KxN],directions')
def best_embedding_on_sphere(R, ndim):
    coords = best_embedding(R, ndim)
    proj = project_vectors_onto_sphere(coords)
    return proj

@contracts(R='array[NxN]', ndim='int,K', returns='array[KxN]')
def best_embedding(R, ndim):
    U, S, V = np.linalg.svd(R, full_matrices=0)
    check_multiple([ ('array[NxN]', U),
                     ('array[N]', S),
                     ('array[NxN]', V) ])
    coords = V[:ndim, :]
    for i in range(ndim):
        coords[i, :] = coords[i, :]  * np.sqrt(S[i])
    return coords

def scale_score(x):
    y = x.copy()
    order = np.argsort(x.flat)
    # Black magic ;-) Probably the smartest thing I came up with today. 
    order_order = np.argsort(order)
    y.flat[:] = order_order.astype(y.dtype)
    return y


def compute_relative_error(true_S, S, neighbours_deg=20):
    ''' Returns the average error in radians between points. '''
    true_C = get_cosine_matrix_from_s(true_S)
    true_D = np.arccos(true_C)
    valid = true_D < np.radians(neighbours_deg)

    C = get_cosine_matrix_from_s(S)
    D = np.arccos(C)
    
    nvalid = (1 * valid).sum()
    errors = np.abs((D - true_D))
    errors_sum = (errors * valid).sum()
    
    average_error = errors_sum / nvalid
    return average_error
    
@contracts(S='array[KxN],K<N', returns='array[KxN]')
def project_vectors_onto_sphere(S, atol=1e-7):
    K, N = S.shape
    coords_proj = np.zeros((K, N))
    for i in range(N):
        v = S[:, i]
        nv = np.linalg.norm(v)
        if np.fabs(nv) < atol:
            raise ValueError('Vector too small: %s' % v)
        coords_proj[:, i] = v / nv
    return coords_proj

def cov2corr(covariance, zero_diagonal=False):
    ''' 
    Compute the correlation matrix from the covariance matrix.
    If zero_diagonal = True, the diagonal is set to 0 instead of 1. 

    :param zero_diagonal: Whether to set the (noninformative) diagonal to zero.
    :param covariance: A 2D numpy array.
    :return: correlation: The exctracted correlation.
    
    '''
    # TODO: add checks
    outer = np.multiply.outer

    sigma = np.sqrt(covariance.diagonal())
    M = outer(sigma, sigma)
    correlation = covariance / M
    
    if zero_diagonal:
        for i in range(covariance.shape[0]):
            correlation[i, i] = 0
    
    return correlation
