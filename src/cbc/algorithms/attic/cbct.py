import numpy as np

from contracts import check

from ..tools  import (scale_score, best_embedding_on_sphere, cosines_from_directions)    
from . import CalibAlgorithm


class CBCt(CalibAlgorithm):
    def _solve(self, R):
        ndim = self.params['ndim']
        num_iterations = self.params['num_iterations']
        trust_R_top_perc = self.params['trust_R_top_perc']
        check('>0,<100', trust_R_top_perc)
        
        # Score of each datum -- must be computed only once
        R_order = scale_score(R).astype('int32')
        R_percentile = R_order * 100.0 / R_order.size
        
        M = (R_order * 2.0 / (R.size - 1)) - 1
        np.testing.assert_almost_equal(M.max(), +1)
        np.testing.assert_almost_equal(M.min(), -1)

        current_guess_for_S = best_embedding_on_sphere(M, ndim)
        
        for iteration in range(num_iterations):
            guess_for_C = cosines_from_directions(current_guess_for_S)
            guess_for_C_sorted = np.sort(guess_for_C.flat)
            new_estimated_C = guess_for_C_sorted[R_order]
            
            careful_C = new_estimated_C.copy()
            dont_trust = R_percentile < (100 - trust_R_top_perc)
#            if iteration > 0:
            careful_C[dont_trust] = guess_for_C[dont_trust]
#                careful_C[dont_trust] = -1 # good for fov 360
#                careful_C[dont_trust] = 0
                

            new_guess_for_S = best_embedding_on_sphere(careful_C, ndim) 
            
            data = dict(S=new_guess_for_S, **locals())
            self.iteration(data)
            
            current_guess_for_S = new_guess_for_S
            
    # Prove fixed point:
    # :: guess_for_S = true_S
    # guess_for_C = get_cosine_matrix_from_s(guess_for_S)
    # :: guess_for_C = true_C
    # guess_for_C_sorted = np.sort(guess_for_C.flat)
    # :: guess_for_C_sorted = sort(true_C)
    # new_estimated_C = guess_for_C_sorted[R_order]
    # :: new_estimated_C = (sort(true_C))[R_order]
    #    by assumption (R=g(C), g monotone), we have R_order = C_order
    # :: new_estimated_C = (sort(true_C))[order(true_C)]
    #    For all vectors x, sort(x)[order(x)] = x
    # :: new_estimated_C = true_C
    #    new_guess_for_S = best_embedding_on_sphere(new_estimated_C, ndim)
    # :: new_guess_for_S = best_embedding_on_sphere(true_C, ndim)
    #    new_guess_for_S = true_S
