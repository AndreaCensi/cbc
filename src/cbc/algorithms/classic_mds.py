from ..tools  import scale_score    
import numpy as np
from . import CalibAlgorithm
from geometry import mds
from .base import EUCLIDEAN

class EuclideanMDS(CalibAlgorithm):
    def __init__(self, params):
        CalibAlgorithm.__init__(self, params, geometry=EUCLIDEAN)
        
    def _solve(self, R):
        ndim = self.params['ndim']
         
        D0 = R.max() - R 
        np.testing.assert_almost_equal(D0.min(), 0)
        np.testing.assert_allclose(D0[0, 0], 0)

        S = mds(D0, ndim)
        self.iteration(dict(S=S))

