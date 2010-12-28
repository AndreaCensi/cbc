import numpy as np

from . import CalibAlgorithm

from ..tools  import (scale_score, best_embedding_on_sphere,
                      get_cosine_matrix_from_s)

class CBC(CalibAlgorithm):
    def _solve(self, R):
        ndim = self.params['ndim']
        num_iterations = self.params['num_iterations']
        
        # Score of each datum -- must be computed only once
        R_order = scale_score(R).astype('int32')

        M = (R_order * 2.0 / (R.size - 1)) - 1
        np.testing.assert_almost_equal(M.max(), +1)
        np.testing.assert_almost_equal(M.min(), -1)
        current_guess_for_S = best_embedding_on_sphere(M, ndim)

        for iteration in range(num_iterations):
            guess_for_C = get_cosine_matrix_from_s(current_guess_for_S)
            guess_for_C_sorted = np.sort(guess_for_C.flat)
            new_estimated_C = guess_for_C_sorted[R_order]
            new_guess_for_S = best_embedding_on_sphere(new_estimated_C, ndim) 
            
            data = dict(S=new_guess_for_S, **locals())
            self.iteration(data)
            
            current_guess_for_S = new_guess_for_S
