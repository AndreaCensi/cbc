from . import np
import itertools
from . import svds, contract
from ..tools import (best_embedding_on_sphere, \
     distances_from_directions, assert_allclose)
from numpy.core.numeric import allclose
import sys

def f():
    d = np.pi / 3
    
    D = np.zeros((6, 6))
    D[:] = np.nan
    
    A, B, C = 0, 1, 2
    ab, bc, ca = 3, 4, 5
    
    D[A, B] = D[B, C] = D[C, A] = d
    
    D[A, ab] = D[B, ab] = 0.5 * d 
    D[A, ca] = D[C, ca] = 0.5 * d
    D[C, bc] = D[B, bc] = 0.5 * d
    D[ab, bc] = D[bc, ca] = D[ca, ab] = d * 0.5
    
    D[A, bc] = D[B, ca] = D[C, ab] = d # XXX
    
    for i, j in itertools.product(range(6), range(6)):
        if np.isnan(D[i, j]) and not np.isnan(D[j, i]):
            D[i, j] = D[j, i]
    for i in range(6):
        D[i, i] = 0
        
        
    print D
    
    some = svds(np.cos(D), 10)
    
    print list(some)
    
def f2():
    D = np.zeros((3, 3))
    D[:] = np.nan
    
    A, B, C = 0, 1, 2
    
    ab, bc, ca = 3, 4, 5
    
    names = {A:'A', B:'B', C:'C', ab:'ab', bc:'bc', ca:'ca'}
    
    d = np.pi / 25
    D[A, B] = D[B, C] = D[C, A] = d
    
    fillD(D)
    
    
#    some = svds(np.cos(D), 10)
#    
    S = best_embedding_on_sphere(np.cos(D), 3)
    
    S2 = np.zeros((3, 6))
    for i in range(3): S2[:, i] = S[:, i]
    
    S2[:, ab] = midpoint_on_sphere(S[:, A], S[:, B])
    S2[:, bc] = midpoint_on_sphere(S[:, B], S[:, C])
    S2[:, ca] = midpoint_on_sphere(S[:, C], S[:, A])
    
    D2 = distances_from_directions(S2)
    
    @contract(x='array[MxN]')
    def pprint(x, format='%.3f'): #@ReservedAssignment
        for a in range(x.shape[0]):
            sys.stdout.write('[')
            for b in range(x.shape[1]):
                sys.stdout.write(format % x[a, b])
                sys.stdout.write(', ')
            sys.stdout.write(']\n')
    pprint(D2, '%.2f')
    
    S3 = best_embedding_on_sphere(np.cos(D2), 3)
    D2 = distances_from_directions(S3)
    
    assert_allclose(D[A, B], 2 * D2[A, ab])
    assert_allclose(D[A, C], 2 * D2[A, ca])
    assert_allclose(D[C, B], 2 * D2[C, bc])
    
    for t in [ [A, B, C],
              [ab, bc, ca],
              [A, ab, ca],
              [B, ab, bc],
              [C, ca, bc]]:
        x, y, z = t
        d = [D2[x, y], D2[y, z], D2[z, x]]
        equil = allclose(d[0], d[1]) and allclose(d[1], d[2])
        name = '-'.join(names[x] for x in t)
        mark = '(equiv)' if equil else ""
        print('Triangle %s: %.2f %.2f %.2f %s' % (name, d[0], d[1], d[2], mark))
              
    
    
@contract(s1='direction', s2='direction')
def midpoint_on_sphere(s1, s2):
    if allclose(s1, -s2): # TODO: add precision
        raise ValueError()
    else:
        v = (s1 + s2) * 0.5
        return v / np.linalg.norm(v)
    
def fillD(D):
    n = D.shape[0]
    for i, j in itertools.product(range(n), range(n)):
        if np.isnan(D[i, j]) and not np.isnan(D[j, i]):
            D[i, j] = D[j, i]
            
    for i in range(n):
        D[i, i] = 0

    
f2()
     
