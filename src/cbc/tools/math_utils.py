from . import np, contract, new_contract
from ..tools import distribution_radius


def create_histogram_2d(x, y, resolution):
    edges = np.linspace(-1, 1, resolution)
    H, _, _ = np.histogram2d(x.flatten(), y.flatten(), bins=(edges, edges))
    return H

new_contract('cosines', 'array[NxN](>=-1,<=+1)')
# new_contract('angles', 'array[N](>=-pi,<pi)')
new_contract('distances', 'array[NxN](>=0,<=pi)')


@contract(theta='array[N]', returns='array[2xN], directions')
def directions_from_angles(theta):
    return np.vstack((np.cos(theta), np.sin(theta)))


@contract(S='array[KxN], directions', returns='array[N], angles')
def angles_from_directions(S):
    if S.shape[0] > 2: # TODO: make contract
        assert (S[2, :] == 0).all()
    return np.arctan2(S[1, :], S[0, :])


@contract(S='array[KxN], directions', returns='array[NxN], cosines')
def cosines_from_directions(S):
    C = np.dot(S.T, S)
    return np.clip(C, -1, 1, C)


@contract(C='array[NxN], cosines', returns='array[NxN], distances')
def distances_from_cosines(C):
    return np.real(np.arccos(C))


@contract(D='distances', returns='cosines')
def cosines_from_distances(D):
    return np.cos(D)


@contract(S='directions', returns='distances')
def distances_from_directions(S):
    C = cosines_from_directions(S)
    return distances_from_cosines(C)


def scale_score(x):
    y = x.copy()
    order = np.argsort(x.flat)
    # Black magic ;-) Probably the smartest thing I came up with today. 
    order_order = np.argsort(order)
    y.flat[:] = order_order.astype(y.dtype)
    return y


def compute_relative_error(true_S, S, neighbours_deg=20):
    ''' Returns the average error in radians between points. '''
    # TODO: make default to consider all (URG compute_relative_error)
    true_C = cosines_from_directions(true_S)
    true_D = np.arccos(true_C)
    valid = true_D < np.radians(neighbours_deg)

    C = cosines_from_directions(S)
    D = np.arccos(C)

    nvalid = (1 * valid).sum()
    errors = np.abs((D - true_D))
    errors_sum = (errors * valid).sum()

    average_error = errors_sum / nvalid
    return average_error


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


@contract(S='directions', returns='direction')
def mean_directions(S):
    # Find "center" of distribution:
#    x = S[0, :].mean()
#    y = S[1, :].mean()
#    center = np.arctan2(y, x)
    x = S.mean(axis=1)
    xn = np.linalg.norm(x)
    if xn == 0:
        return np.array([1, 0, 0])
    else:
        return x / xn


@contract(S='directions', returns='float,>0,<=6.29')
def compute_diameter(S):
    return 2 * distribution_radius(S)
##    
#    x = S[0, :].mean()
#    y = S[1, :].mean()
#    center = np.arctan2(y, x)
#    angles = angles_from_directions(S)
#    differences = normalize_pi(angles - center)
#    diameter = differences.max() - differences.min()
#    return diameter
#    


@contract(x='array[N]', ref='array[N]', mod='int', returns='array[N]')
def find_closest_multiple(x, ref, mod):
    ''' Find the closest multiple of x (wrt mod) to the element in ref. '''
    def neg_mod(c, mod):
        c = c % mod
        if c > mod / 2:
            c -= mod
        return c

    res = np.empty_like(x)
    for i in range(x.size):
        xi = x.flat[i]
        refi = ref.flat[i]
        res.flat[i] = refi + neg_mod(xi - refi, mod)
    return res


@contract(x='array,shape(x)', y='array,shape(x)', returns='float,<=1,>=-1')
def correlation_coefficient(x, y):
    ''' Returns the correlation between two sequences. '''
    correlation_matrix = np.corrcoef(x.flat, y.flat)
    assert correlation_matrix.shape == (2, 2)
    return np.clip(correlation_matrix[0, 1], -1.0, 1.0)


