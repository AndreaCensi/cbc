import pickle 
from nose.tools import nottest 

from contracts import contracts 
from cbc.test_cases import CalibTestCase 
from .synthetic import Ticker
import os

@nottest
@contracts(returns='dict(str: tuple(Callable, dict))')
def get_mino_testcases(directory):
    print('Loading Mino data from disk...')
    sets = ['mino1_grid24',
            'mino1_center',
            'mino1_middle',
            'mino1_midcen',
            'mino1_patch32',
            'mino1_patch32s4',
            'mino1_grid24art',
            'mino1_centerart',
            'mino1_middleart',
            'mino1_midcenart',
            'mino1_patch32art',
            'mino1_patch32s4art']
    
    
    tcs = {}
    ticker = Ticker('Generating real cases')
    def add_test_case(tcid, function, args):
        ticker(tcid)
        tcs[tcid] = (function, args)

    for s in sets:
        filename = os.path.join(directory, '%s_stats.pickle' % s)
        with open(filename) as f: 
            data = pickle.load(f)
            
        R = data['y_corr']
        S = data['true_S']
        tcid = '%s-y_corr' % s 
        add_test_case(tcid, test_case, dict(tcid=tcid, R=R, S=S, kernel=None))

    return tcs

def test_case(tcid, R, S, kernel):
    tc = CalibTestCase(tcid, R)
    if S is not None:
        tc.set_ground_truth(S, kernel=kernel)
    return tc
 
 
