from . import contract, new_contract
from ..tools import (cosines_from_directions, distances_from_cosines,
    euclidean_distances)


# TODO: decorator
class CalibTestCase(object):
    
    @contract(tcid=str, R='array[NxN]')
    def __init__(self, tcid, R, geometry='S'):
        self.tcid = tcid
        self.R = R
        self.has_ground_truth = False
        self.geometry = geometry

    @contract(S='array[(2|3)xN]', kernel='None|Callable')        
    def set_ground_truth(self, S, kernel):
        self.has_ground_truth = True
        self.true_S = S
        if self.is_spherical():
            self.true_C = cosines_from_directions(self.true_S)
            self.true_D = distances_from_cosines(self.true_C)
        if self.is_euclidean():
            self.true_D = euclidean_distances(self.true_S)
        self.true_kernel = kernel
        
    def is_spherical(self):
        return self.geometry == 'S'
    
    def is_euclidean(self):
        return self.geometry == 'E'
    

new_contract('test_case', CalibTestCase)
