import numpy as np

from snp_geometry import assert_allclose, random_directions

from cbc.tools import cosines_from_directions, \
    best_embedding_on_sphere, \
    overlap_error_after_orthogonal_transform, \
    angles_from_directions, directions_from_angles
import time
from contracts.enabling import disable_all 

def get_angles_from_S_test():
    theta = np.random.rand(120) * np.pi * 2 - np.pi 
    S = directions_from_angles(theta)
    theta2 = angles_from_directions(S)
    assert_allclose(theta, theta2)

def best_embedding_test():
    for i in range(10): #@UnusedVariable
        n = 10 + i * 100
        
        S = random_directions(n)
        t = time.clock()
        C = cosines_from_directions(S)
        T2 = time.clock() - t
        
        t = time.clock()
        S2 = best_embedding_on_sphere(C, ndim=3)
        T0 = time.clock() - t 
        
        t = time.clock()
        error = overlap_error_after_orthogonal_transform(S, S2)
        assert_allclose(error, 0, atol=1e-6)
        T1 = time.clock() - t 
        
        print('Embedding %d: %.2f %.2f %.2f seconds' % (n, T2, T0, T1))

def test_best_embedding_2d():
    for i in range(10): #@UnusedVariable
        n = 10 + i * 100
        S = directions_from_angles(np.random.rand(n) * np.pi * 2)
        C = cosines_from_directions(S)
        S2 = best_embedding_on_sphere(C, ndim=2)
        error = overlap_error_after_orthogonal_transform(S, S2)
        assert_allclose(error, 0, atol=1e-6)
                 
if __name__ == '__main__': 
    disable_all()
    import cProfile
    file = 'prof'
    cProfile.run('best_embedding_test()', file)
    import pstats
    p = pstats.Stats(file)
    p.sort_stats('cumulative').print_stats(20)
        
