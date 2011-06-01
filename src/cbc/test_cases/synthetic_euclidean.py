import numpy as np
import itertools
from nose.tools import nottest

from contracts import contracts, decorate 
 
from . import CalibTestCase 
from .utils import Ticker, add_distance_noise

from geometry import euclidean_distances 

kernels = []
def k(f):
    signature = dict(d='array(>=0,<=pi),shape(x)',
                     returns='array(>=-1,<=+1),shape(x)')
    f2 = decorate(f, **signature)
    kernels.append(f2)
    return f2

DIAMETER = np.pi

# Kernels are functions from cosine -> correlation ([-1,1]->[-1,1])
# The should be able to operate on arrays and return arrays
def saturate(f, d): return f(np.minimum(1, d))
#def saturate(f, d): return f(np.minimum(DIAMETER / 2, d))

@k
def eu_linear01(d): return (1 - d / DIAMETER)
@k
def eu_linear01_sat(d): return saturate(eu_linear01, d)

@k
def eu_pow3(d): return np.cos(d) ** 3
@k
def eu_pow3_sat(d): return saturate(eu_pow3, d)
@k
def eu_pow7(d): return np.cos(d) ** 7
@k
def eu_pow7_sat(d): return saturate(eu_pow7, d)



@nottest
@contracts(returns='dict(str: tuple(Callable, dict))')
def get_euclidean_test_cases():
    # check that we don't have repeated names
    all_names = [f.__name__ for f in kernels]
    assert len(all_names) == len(np.unique(all_names)), \
        'Repeated names for kernels: %s' % all_names
    
    tcs = {}

    ticker = Ticker('Generating synthetic euclidean cases')
    def add_test_case(tcid, function, args):
        ticker(tcid)
        tcs[tcid] = (function, args)
    
    num = 180
    dims = [2, 3]
    dist_noise = 0.01
#    dist_noise = 0
    wiggle_noise = 0.03
    
    for kernel, ndim in itertools.product(kernels, dims):
        tcid = 'E%d-rand-n%d-%s' % (ndim, num, kernel.__name__)
        func = generate_random_euclidean_test_case
        args = dict(tcid=tcid,
                     num=num,
                     ndim=ndim,
                     kernel=kernel,
                     dist_noise=dist_noise)
        add_test_case(tcid, func, args)

    for kernel, ndim in itertools.product(kernels, dims):
        tcid = 'E%d-grid-n%d-%s' % (ndim, num, kernel.__name__)
        func = generate_grid_euclidean_test_case
        args = dict(tcid=tcid,
                     num=num,
                     ndim=ndim,
                     kernel=kernel,
                     dist_noise=dist_noise,
                     wiggle_noise=wiggle_noise)
        add_test_case(tcid, func, args)

    return tcs


def generate_random_euclidean_test_case(tcid, num, ndim, kernel, dist_noise):
    S = np.random.rand(ndim, num) - 0.5
    S = S * np.sqrt(DIAMETER)
    D = euclidean_distances(S)
    D2 = add_distance_noise(D, dist_noise)
    R2 = kernel(D2) 
    tc = CalibTestCase(tcid, R2, geometry='E')
    tc.set_ground_truth(S, kernel)
    return tc

def generate_grid_euclidean_test_case(tcid, num, ndim, kernel, wiggle_noise, dist_noise):
    assert ndim == 2
    side = int(np.ceil(np.sqrt(num)))
    num = side * side
    k = 0
    
    def wiggle(): return np.random.randn()*wiggle_noise
    
    S = np.zeros((ndim, num))
    for i, j in itertools.product(range(side), range(side)):
        S[0, k] = (i - side / 2.0) / side + wiggle()
        S[1, k] = (j - side / 2.0) / side + wiggle()
        k += 1
    S = S * np.sqrt(DIAMETER)
    D = euclidean_distances(S)
    D2 = add_distance_noise(D, dist_noise)
    R2 = kernel(D2) 
    tc = CalibTestCase(tcid, R2, geometry='E')
    tc.set_ground_truth(S, kernel)
    return tc
