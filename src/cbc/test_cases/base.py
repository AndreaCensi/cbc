from contracts import contracts
from contracts.main import new_contract
from cbc.tools.math_utils import get_distance_matrix_from_cosine, \
    get_cosine_matrix_from_s

# TODO: decorator
class CalibTestCase(object):
    
    @contracts(tcid=str, R='array[NxN]')
    def __init__(self, tcid, R):
        self.tcid = tcid
        self.R = R
        self.has_ground_truth = False

    @contracts(S='array[(2|3)xN]', kernel='None|Callable')        
    def set_ground_truth(self, S, kernel):
        self.has_ground_truth = True
        self.true_S = S
        self.true_C = get_cosine_matrix_from_s(self.true_S)
        self.true_D = get_distance_matrix_from_cosine(self.true_C)
        self.true_kernel = kernel

new_contract('test_case', CalibTestCase)
