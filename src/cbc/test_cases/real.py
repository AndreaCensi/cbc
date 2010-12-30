import numpy as np
from nose.tools import nottest
import itertools

from contracts import contracts, check

from ..tools import cov2corr, directions_from_angles
from . import CalibTestCase

@nottest
@contracts(data=dict, returns='dict(str: test_case)')
def get_real_test_cases(data):
    # two types
    selections = [ ('sick_front', np.array(range(181))),
                   ('sick_rear', np.array(range(181, 362))),
                   ('sick_both', np.array(range(362))) ]
    
    # four different statistics
    def stat(var):
        x = data['%s_cov' % var]
        R = cov2corr(x, False)
        return (var, R)
    
    statistics = [ stat('y'),
                   stat('y_dot'),
                   stat('y_dot_sign'),
                   stat('y_dot_abs')]
    
    check('list(tuple(str, $(array[M], M>0, M<=362) ))', selections)
    check('list(tuple(str, array[362x362]))', statistics)
    
    ground_truth = np.linspace(0, np.pi * 2, 362)
    
    tcs = {}
    for sel, stat in itertools.product(selections, statistics):
        selid, select = sel
        statid, bigR = stat
        
        R = bigR[select, :][:, select]
        
        angles = ground_truth[select]
        S = directions_from_angles(angles)
        
        tcid = '%s-%s' % (selid, statid)
        tc = CalibTestCase(tcid, R)
        tc.set_ground_truth(S, kernel=None)
        
        tcs[tcid] = tc
        
    return tcs
