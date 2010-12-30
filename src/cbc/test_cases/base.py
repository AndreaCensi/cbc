from contracts import contracts
from contracts.main import new_contract
from ..tools.math_utils import cosines_from_directions, distances_from_cosines


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
        self.true_C = cosines_from_directions(self.true_S)
        self.true_D = distances_from_cosines(self.true_C)
        self.true_kernel = kernel

new_contract('test_case', CalibTestCase)
