import numpy as np
from collections import namedtuple

from ..tools import best_embedding_on_sphere, overlap_error_after_orthogonal_transform

def random_sample(n, k):
    x = range(n)
    np.random.shuffle(x)
    return x[:k]
    
def get_ratios(min_ratio, max_ratio, n):
    ratios = np.exp(np.linspace(np.log(min_ratio), np.log(max_ratio), n - 1))
    ratios = np.array(sorted(ratios.tolist() + [1.0])) # always include 1.0 
    return ratios


ScaleResult = namedtuple('ScaleResult',
    'S ratio ratios measure error_deg')

print('ciao')
def warp_fit(D, min_ratio, max_ratio, nratios,
                  nlandmarks, ndim=3, true_S=None, true_alpha=None):
    
    # subsample
    n = D.shape[0]
    i = random_sample(n, nlandmarks)
    Di = D[i, :][:, i]

    ratios = get_ratios(min_ratio, max_ratio, nratios)
    
    measure = np.zeros(nratios)

    SS = np.zeros((len(ratios), Di.shape[0]))
    SSn = np.zeros((len(ratios), Di.shape[0]))
    for l, ratio in enumerate(ratios):
        Ci = np.cos(ratio * Di)
        Ci = Ci + Ci.T
        ev = np.linalg.eigvals(Ci)
        ev = np.abs(ev)
        SS[l, :] = ev
        SSn[l, :] = SS[l, :] / SS[l, 0] 
        measure[l] = SSn[l, 2] / SSn[l, 3]
        
        print('ratio: %.3f  measure: %.3f' % (ratio, measure[l]))
    
    classifica = np.argsort(-measure)
    best_ratio = ratios[classifica[0]]
    print('Best ratio: %s' % best_ratio)
    
    C = np.cos(best_ratio * D)
    S = best_embedding_on_sphere(C, ndim)
    
    if true_S is not None:
        error_deg = np.rad2deg(overlap_error_after_orthogonal_transform(S, true_S))
    else:
        error_deg = None
    
    return ScaleResult(S=S, ratio=best_ratio, ratios=ratios, measure=measure,
                error_deg=error_deg)
