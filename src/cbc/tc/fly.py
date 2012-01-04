from . import np, check, pickle, test_case
from ..tools import cov2corr


def get_fly_testcase(filename):
    print('Loading fly data...')

    with open(filename) as f:
        data = pickle.load(f)
    print('...done.')

    R = cov2corr(data['P'])

    S = data['S'].astype('float64')
    check('array[3xN],N>1000', S)
    check('directions', S)

    # re-normalize directions (numerical errors)
    for i in range(S.shape[0]):
        S[:, i] /= np.linalg.norm(S[:, i])

    return {'fly': (test_case, dict(tcid='fly', S=S, kernel=None, R=R))}

