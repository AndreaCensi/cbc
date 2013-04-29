from contracts import contract
from geometry import rotation_from_axes_spec
import numpy as np
from procgraph import simple_block


@contract(S='array[HxWx3]', ndim='K,(2|3)', returns='array[KxN]')
def flatten_S(S, ndim):
    x = as_1d((S[:, :, 0].squeeze()))
    y = as_1d((S[:, :, 1].squeeze()))
    z = as_1d((S[:, :, 2].squeeze()))
    true_S = np.vstack((x, y, z))

    if ndim == 2:
        return project_2d(true_S)
    else:
        return true_S

@simple_block
def as_1d(x):
    if x.ndim == 2:
        H, W = x.shape
        return x.reshape(H * W)
    else:
        return x


@contract(S='array[3xN],directions', returns='array[3xN], directions')
def project_2d(S):
    """Projects a spherical dist to 2d"""

    # everything should be in between
    a = S[:, 0]
    b = S[:, -1]

    R = rotation_from_axes_spec(a, b)

    n = S.shape[1]
    P = np.zeros((3, n))

    for i in range(n):
        c = S[:, i]
        cc = np.dot(R, c)

        limit = np.sin(np.deg2rad(2))
        if np.abs(cc[2]) > limit:
            angle = np.arcsin(np.abs(cc[2]))
            raise Exception(
                'Expected this to be planar: %s, while it is %s deg above'
                            % (cc, np.rad2deg(angle)))

        # theta = np.arctan2(cc[1], cc[0])

        P[0:2, i] = cc[0:2]
        P[2, i] = 0

        # Normalize
        P[:, i] = P[:, i] / np.linalg.norm(P[:, i])

    return P


@contract(returns='array[(2|3)xN]')
def filter_S(S, filter, ndim):  # @ReservedAssignment
    ''' 
        Filters the ground truth. 
        If ndim==2, a 3D S will be projected down to 2D.
    '''
    x = as_1d(filter(S[:, :, 0].squeeze()))
    y = as_1d(filter(S[:, :, 1].squeeze()))
    z = as_1d(filter(S[:, :, 2].squeeze()))

    true_S = np.vstack((x, y, z))

    if ndim == 2:
        return project_2d(true_S)
    else:
        return true_S


def filter_S_keep_dim(S, filter_function):
    S0 = filter_function(S[:, :, 0])
    S1 = filter_function(S[:, :, 1])
    S2 = filter_function(S[:, :, 2])

    shape = [3]
    shape.extend(S0.shape)
    SS = np.zeros(shape=shape, dtype='float32')
    SS[0, ...] = S0
    SS[1, ...] = S1
    SS[2, ...] = S2
    return SS


def reshape(y, true_S):
    y0 = y[0, ...]
    print('Original')
    print('-      y: %s' % str(y.shape))
    print('-     y0: %s' % str(y0.shape))
    print('- true_S: %s' % str(true_S.shape))
    if y0.size * 3 != true_S.size:
        raise Exception('Incompatible dimensions %s %s' % 
                        (y0.shape, true_S.shape))

    if len(y.shape) == 3:
        N, H, W = y.shape

        yf = np.zeros((N, H * W))
        for i in range(N):
            yf[i, :] = as_1d(y[i, :])
        y = yf

    if true_S is None:
        true_Sf = None
    else:
        if len(true_S.shape) == 3:
            H, W, K = true_S.shape
            assert K == 3, '%s' % K
            true_Sf = np.zeros((3, H * W))
            true_Sf[0, :] = as_1d(true_S[:, :, 0])
            true_Sf[1, :] = as_1d(true_S[:, :, 1])
            true_Sf[2, :] = as_1d(true_S[:, :, 2])
            true_S = true_Sf

    print('Final')
    print('-      y: %s' % str(y.shape))
    print('- true_S: %s' % str(true_S.shape))

    return y, true_S


def desc(name, a):
    if a.dtype == np.dtype('bool'):
        x = np.sum(a)
        y = a.size
        p = 100.0 * x / y
        other = '%s/%s=%.1f%%' % (x, y, p)
    else:
        other = None
    print(' %14s: %s %s %s' % (name, a.dtype, a.shape, other))
