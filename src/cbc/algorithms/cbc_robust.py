from . import CalibAlgorithm
from ..tools import (scale_score, best_embedding_on_sphere,
    cosines_from_directions, distances_from_cosines)
from .warp_fit import warp_fit
import numpy as np
 

class CBC_robust(CalibAlgorithm):
    ''' Starts from either a 2pi or 1pi guess, chooses the best. '''
    def _solve(self, R):
        ndim = self.params['ndim']
        num_iterations = self.params['num_iterations']
        warp = self.params['warp']
        trust_top_perc = self.params['trust_top_perc']
        starting = self.params.get('starting', [1, 2])
        
        # Score of each datum -- must be computed only once
        R_order = scale_score(R).astype('int32')

        Mpi2 = (R_order * 2.0 / (R.size - 1)) - 1
        np.testing.assert_almost_equal(Mpi2.max(), +1)
        np.testing.assert_almost_equal(Mpi2.min(), -1)
        Mpi1 = (Mpi2 + 1) / 2
        np.testing.assert_almost_equal(Mpi1.max(), +1)
        np.testing.assert_almost_equal(Mpi1.min(), 0)
         
        if 1 in starting:
            print('Solving, phase pi1')
            self.solve_from_start(R_order, Mpi1,
                              ndim=ndim, num_iterations=num_iterations,
                              trust_top_perc=trust_top_perc,
                              phase='pi1')
        
        if 2 in starting:
            print('Solving, phase pi2')
            self.solve_from_start(R_order, Mpi2,
                              ndim=ndim, num_iterations=num_iterations,
                              trust_top_perc=trust_top_perc,
                              phase='pi2')

#        measure = 'spearman_robust'
        measure = 'spearman'
        best_iteration = self.get_best_so_far(measure) 
        phase = best_iteration['phase']
        self.iteration(best_iteration)
        
        if warp and ndim > 2:
            C = best_iteration['C']
            D = distances_from_cosines(C)
            r = warp_fit(D, min_ratio=0.1, max_ratio=2, nratios=100,
                  nlandmarks=300, ndim=ndim, true_S=self.true_S)
            print('Solved: ratio=%f error_deg=%s' % (r.ratio, r.error_deg))
            self.iteration(dict(S=r.S, phase='%s_warp_fit' % phase,
                                ratios=r.ratios, measures=r.measure))
             
    
    def get_best_so_far(self, measure='spearman', measure_sign= -1):
        all_spearman = list(x[measure] for x in self.iterations)
        best_scores = np.argsort(measure_sign * np.array(all_spearman))
        best_iteration = self.iterations[best_scores[0]] 
        print('Best so far: #%d (according to %s %d)' % 
              (best_scores[0], measure, measure_sign))
        return best_iteration

    def solve_from_start(self, R_order, M0, ndim, num_iterations, trust_top_perc, phase):
        current_guess_for_S = best_embedding_on_sphere(M0, ndim)

        R_percentile = R_order * 100.0 / R_order.size

        for iteration in range(num_iterations): #@UnusedVariable
            guess_for_C = cosines_from_directions(current_guess_for_S)
            guess_for_C_sorted = np.sort(guess_for_C.flat)
            new_estimated_C = guess_for_C_sorted[R_order]
            not_trusted = R_percentile < (100 - trust_top_perc)
            new_estimated_C[not_trusted] = guess_for_C[not_trusted]
            
            new_guess_for_S = best_embedding_on_sphere(new_estimated_C, ndim) 
            data = dict(S=new_guess_for_S, C=new_estimated_C, phase=phase)
            self.iteration(data)
            
            current_guess_for_S = new_guess_for_S 

