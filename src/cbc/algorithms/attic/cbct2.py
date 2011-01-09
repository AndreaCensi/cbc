import numpy as np

from ..tools  import (scale_score, best_embedding_on_sphere, cosines_from_directions)    
from . import CalibAlgorithm


class CBCt2(CalibAlgorithm):
    def _solve(self, R):
        ndim = self.params['ndim']
        num_iterations = self.params['num_iterations']
#        trust_R_top_perc = self.params['trust_R_top_perc']
#        check('>0,<100', trust_R_top_perc)
        
        # Score of each datum -- must be computed only once
        R_order = scale_score(R).astype('int32')
        R_percentile = R_order * 100.0 / R_order.size
        
        M = (R_order * 2.0 / (R.size - 1)) - 1.0
        np.testing.assert_almost_equal(M.max(), +1)
        np.testing.assert_almost_equal(M.min(), -1)
        current_guess_for_S = best_embedding_on_sphere(M, ndim)
        
        time = [100, 10, 20, 30, 40, 0, 0, 0, 0, 0, 0, 0]# 50, 60, 70, 80, 90, 100, 100, 100]
        for iteration in range(len(time)):
            guess_for_C = cosines_from_directions(current_guess_for_S)
            guess_for_C_sorted = np.sort(guess_for_C.flat)
            new_estimated_C = guess_for_C_sorted[R_order]
            
            careful_C = new_estimated_C.copy()
            D = np.arccos(careful_C)
            print('Current estimated diameter: %s' % np.degrees(D.max()))
            D = D * 0.9
            careful_C = np.cos(D)
            
            trust_R_top_perc = time[iteration]
#            dont_trust = R_percentile < (100 - trust_R_top_perc)
            dont_trust = guess_for_C < -0.2
#            careful_C[dont_trust] = guess_for_C[dont_trust]
#                careful_C[dont_trust] = -1 # good for fov 360
#                careful_C[dont_trust] = 0
                
            new_guess_for_S = best_embedding_on_sphere(careful_C, ndim) 
            
            data = dict(S=new_guess_for_S, **locals())
            self.iteration(data)
            
            current_guess_for_S = new_guess_for_S
         
