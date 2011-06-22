import os
import cPickle as pickle
from . import CalibTestCase 


GT_FILE = 'ground_truth.pickle'
TC_FILE = 'stats.pickle'

def load_test_case(dirname):
    tcid = os.path.basename(dirname)
    stats = os.path.join(dirname, TC_FILE)
    data = pickle.load(open(stats,'rb'))
    R = data['similarity']
    tc = CalibTestCase(tcid, R)
    
    ground_truth = os.path.join(dirname, 'ground_truth.pickle')
    if os.path.exists(ground_truth):
        S = pickle.load(open(ground_truth,'rb'))['true_S']
        tc.set_ground_truth(S, kernel=None)
        # TODO: add kernel
    return tc
 
 
def write_test_case(dirname, tc):
     basename = os.path.basename(dirname)
     assert dirname == tc.tcid
     # FIXME incomplete
 