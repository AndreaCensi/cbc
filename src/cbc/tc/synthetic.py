from . import CalibTestCase, contract, np, add_distance_noise, nottest
from ..tools import (distances_from_directions, cosines_from_distances,
    directions_from_angles, cosines_from_directions, random_directions_bounded)
from ..utils import Ticker
from contracts import decorate, check
import itertools

        

kernels = []
def k(f):
    signature = dict(x='array(>=-1,<=+1),shape(x)',
                     returns='array(>=-1,<=+1),shape(x)')
    f2 = decorate(f, **signature)
    kernels.append(f2)
    return f2

# Kernels are functions from cosine -> correlation ([-1,1]->[-1,1])
# The should be able to operate on arrays and return arrays
def saturate(f, x): return f(np.maximum(0, x))

@k
def linear01(x): return (x + 1) / 2
@k
def linear01_sat(x): return saturate(linear01, x)

@k
def pow3(x): return x ** 3
@k
def pow3_sat(x): return saturate(pow3, x)
@k
def pow7(x): return x ** 7
@k
def pow7_sat(x): return saturate(pow7, x)

@k
def pow3f(x): return linear01(x) ** 3
@k
def pow7f(x): return linear01(x) ** 7


@nottest
@contract(returns='dict(str: tuple(Callable, dict))')
def get_syntethic_test_cases():
    # check that we don't have repeated names
    all_names = [f.__name__ for f in kernels]
    assert len(all_names) == len(np.unique(all_names)), \
        'Repeated names for kernels: %s' % all_names
    
    fovs_deg = [ 45, 90, 135, 180, 180 + 45, 270, 270 + 45, 360]
    
    num = 180
    tcs = {}
    
    ticker = Ticker('Generating synthetic cases')
    def add_test_case(tcid, function, args):
        ticker(tcid)
        tcs[tcid] = (function, args)
    
    
    for kernel, fov_deg in itertools.product(kernels, fovs_deg):
        tcid = 'fov%d-%s-noisy' % (fov_deg, kernel.__name__)
        func = generate_circular_test_case
        args = dict(tcid=tcid,
                     num=num,
                     fov=np.radians(fov_deg),
                     kernel=kernel,
                     wiggle_std_deg=1,
                     dist_noise=0.1,
                     abs_cos_noise_std=0.1)
        add_test_case(tcid, func, args)


        tcid = 'fov%d-%s' % (fov_deg, kernel.__name__)
        func = generate_circular_test_case
        args = dict(tcid=tcid,
                     num=num,
                     fov=np.radians(fov_deg),
                     kernel=kernel,
                     wiggle_std_deg=1,
                     dist_noise=0.01,
                     abs_cos_noise_std=0.01)
        add_test_case(tcid, func, args)


    for ndim, kernel, fov_deg in itertools.product([2, 3], kernels, fovs_deg):
        tcid = 'rand-%dD-fov%d-%s-zero' % (ndim, fov_deg, kernel.__name__)
        func = generate_random_test_case
        args = dict(tcid=tcid,
                     num=num,
                     ndim=ndim,
                     fov=np.radians(fov_deg),
                     kernel=kernel,
                     dist_noise=0,
                     abs_cos_noise_std=0)
        add_test_case(tcid, func, args)

        tcid = 'rand-%dD-fov%d-%s-noisy' % (ndim, fov_deg, kernel.__name__)
        func = generate_random_test_case
        args = dict(tcid=tcid,
                     num=num,
                     ndim=ndim,
                     fov=np.radians(fov_deg),
                     kernel=kernel,
                     dist_noise=0.01,
                     abs_cos_noise_std=0.01)
        add_test_case(tcid, func, args)

    return tcs


@nottest
@contract(tcid=str, num='int,>0', ndim='2|3', fov='<6.29', # XXX: pi
           kernel='Callable', returns='test_case')
def generate_random_test_case(tcid, ndim, fov, num, kernel,
                                dist_noise=0, abs_cos_noise_std=0):
    
    S = random_directions_bounded(ndim=ndim, radius=fov / 2, num_points=num)
    check('directions', S)
    
    C = cosines_from_directions(S)
    # get real distances
    D = np.arccos(C)
    # Multiplicative noise
    noise = np.random.randn(*(D.shape))
    D2 = D + dist_noise * D * noise
    C2 = np.cos(D2)
    
    R = kernel(C2)
    
    # We don't want to mess with the diagonal
    where = R < 5 * abs_cos_noise_std
    R2 = R + where * np.random.randn(*(R.shape)) * abs_cos_noise_std
    
    R2 = np.clip(R2, -1, 1)
    tc = CalibTestCase(tcid, R2)
    tc.set_ground_truth(S, kernel)
    return tc



@nottest
@contract(tcid=str, num='int,>0', kernel='Callable', returns='test_case')
def generate_circular_test_case(tcid, fov, num, kernel,
                                wiggle_std_deg=0, dist_noise=0, abs_cos_noise_std=0):
    angles = np.linspace(-fov / 2, fov / 2, num)
    
    # wiggles the angles a little bit
    angles += np.random.randn(num) * np.radians(wiggle_std_deg)
        
    S = directions_from_angles(angles)
    D = distances_from_directions(S)
    D2 = add_distance_noise(D, dist_noise)
    C2 = cosines_from_distances(D2)
    
    R = kernel(C2)
    
    # We don't want to mess with the diagonal
    where = R < 5 * abs_cos_noise_std
    R2 = R + where * np.random.randn(*(R.shape)) * abs_cos_noise_std
    
    # Make sure R2 is symmetric
    R2 = (R2 + R2.T) / 2
    R2 = np.clip(R2, -1, 1)
    tc = CalibTestCase(tcid, R2)
    tc.set_ground_truth(S, kernel)
    return tc
