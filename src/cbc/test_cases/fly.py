import cPickle as pickle
import os
import numpy as np
from contracts import check

from . import CalibTestCase
from ..tools import cov2corr

def get_fly_testcase():
    print('Loading fly data...')
    filename = os.path.join(os.path.dirname(__file__), 'fly.pickle')
    with open(filename) as f: 
        data = pickle.load(f)
    print('...done.')
    R = cov2corr(data['P'])
    
    tc = CalibTestCase('fly', R)
    
    S = data['S'].astype('float64')
    check('array[3xN],N>1000', S)
    check('directions', S)
    
    # re-normalize directions
    for i in range(S.shape[0]):
        S[:, i] /= np.linalg.norm(S[:, i])
        
    
    tc.set_ground_truth(S, kernel=None)

    return {'fly': tc}
