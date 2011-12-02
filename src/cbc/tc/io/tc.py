from . import contract, new_contract
from ...tools import (cosines_from_directions, distances_from_cosines,
    euclidean_distances)

SPHERICAL = 'S'
EUCLIDEAN = 'E'
GEOMETRIES = [SPHERICAL, EUCLIDEAN]

# TODO: decorator
class CalibTestCase(object):
    
    @contract(tcid=str, R='array[NxN]')
    def __init__(self, tcid, R, geometry=SPHERICAL, attrs={}):
        assert geometry in GEOMETRIES
        self.tcid = tcid
        self.R = R
        self.has_ground_truth = False
        self.geometry = geometry
        self.attrs = attrs

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
        return self.geometry == SPHERICAL
    
    def is_euclidean(self):
        return self.geometry == EUCLIDEAN
    
    def write(self, dirname):
        from . import tc_write_11
        true_S = self.true_S if self.has_ground_truth else None
        tc_write_11(dirname, self.tc_id,
                    self.R, true_S=true_S, geometry=self.geometry, attrs={})

new_contract('test_case', CalibTestCase)
