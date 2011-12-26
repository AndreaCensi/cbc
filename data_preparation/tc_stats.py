import numpy as np
from cbc.tools import distances_from_directions
from contracts import contract


def y_corr(Y, true_S):
    R = np.corrcoef(Y, rowvar=0)
    return R.astype('float32')


def y_corr_m(Y, true_S):
    Y2 = Y.copy().astype('float32')
    Y2 = np.sqrt(Y2)
#    for i in range(Y2.shape[0]):
#        Y2[i, :] -= np.mean(Y2[i, :])
    return y_corr(Y2, true_S)


def y_dot_corr(Y, true_S):
    y0 = Y[:-1, :].astype('float32')
    y1 = Y[+1:, :].astype('float32')
    Y = y1 - y0
    R = np.corrcoef(Y, rowvar=0)
    return R.astype('float32')


def y_dot_sign_corr(Y, true_S):
    y0 = Y[:-1, :].astype('float32')
    y1 = Y[+1:, :].astype('float32')
    Y = y1 - y0
    Y = np.sign(Y)
    R = np.corrcoef(Y, rowvar=0)
    return R.astype('float32')


def artificial(Y, true_S):
    if true_S is None:
        return None

    print('Computing correlation')
    true_D = distances_from_directions(true_S)

    def exponential_kernel(D, alpha):
        return np.exp(-D / alpha)
    R = exponential_kernel(true_D, alpha=0.52)

    return R.astype('float32')


@contract(Y='array[KxN],N<K')
def y_corr_norm(Y, true_S):
    y0 = Y[:-1, :].astype('float32')
    y1 = Y[+1:, :].astype('float32')
    y_dot = y1 - y0

    y_dot_norm = np.sum(y_dot * y_dot, axis=1)
    order = np.argsort(-y_dot_norm)
    # We want them in decreasing order
    assert y_dot_norm[order[0]] > y_dot_norm[order[-1]]
    fraction = 0.5
    largest = order[:int(len(order) * fraction)]

    Y = Y[largest, :]

    R = np.corrcoef(Y, rowvar=0)
    return R.astype('float32')


