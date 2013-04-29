from . import np
from ..tools import (best_embedding_on_sphere,
    overlap_error_after_orthogonal_transform)
from collections import namedtuple


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


def warp_fit(D, min_ratio, max_ratio, nratios,
                  nlandmarks, ndim=3, true_S=None, random=False):

    # subsample
    n = D.shape[0]

    if not(random):
        interval = int(np.ceil(n * 1.0 / nlandmarks))
        i = range(0, n, interval)
        print('Using every other %d: %s' % (interval, i))
    else:
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
        measure_3_4 = SSn[l, 2] / SSn[l, 3]
        measure_123 = np.sum(SSn[l, :3]) / np.sum(SSn[l, 3:])
        measure_4s = -np.sum(SSn[l, 3:])
        measure_3_4s = SSn[l, 2] / np.sum(SSn[l, 3])
        measure[l] = measure_3_4 # This is the one that worked
#        measure[l] = measure_4s
        print(('ratio: %.3f  (1/ratio: %.3f)  *M(s[2]/s[3]): %.3f '
               ' M(sum(:3)/sum(3:)): %.3f '
              '  M(-sum(4:) = %.3f  %.3f ')
              % (ratio, 1.0 / ratio, measure_3_4, measure_123,
                  measure_4s, measure_3_4s))

    classifica = np.argsort(-measure)
    best_ratio = ratios[classifica[0]]
    print('Best ratio: %.3f  (1/ratio: %.3f)' % (best_ratio, 1 / best_ratio))

    C = np.cos(best_ratio * D)
    S = best_embedding_on_sphere(C, ndim)

    if true_S is not None:
        error_deg = np.rad2deg(
                        overlap_error_after_orthogonal_transform(S, true_S))
    else:
        error_deg = None

    return ScaleResult(S=S, ratio=best_ratio, ratios=ratios, measure=measure,
                error_deg=error_deg)
