import numpy as np

from . import CalibAlgorithm

from ..tools  import (scale_score, best_embedding_on_sphere,
                      cosines_from_directions,
                      directions_from_angles,
                      normalize_pi,
                      distances_from_directions,
                      angles_from_directions,
                      cosines_from_distances, assert_allclose)



class CBCchoose(CalibAlgorithm):
    ''' Starts from either a 2pi or 1pi guess, chooses the best. '''
    def _solve(self, R):
        ndim = self.params['ndim']
        num_iterations = self.params['num_iterations']
        warp = self.params['warp']
        
        # Score of each datum -- must be computed only once
        R_order = scale_score(R).astype('int32')

        Mpi2 = (R_order * 2.0 / (R.size - 1)) - 1
        np.testing.assert_almost_equal(Mpi2.max(), +1)
        np.testing.assert_almost_equal(Mpi2.min(), -1)
        Mpi1 = (Mpi2 + 1) / 2
        np.testing.assert_almost_equal(Mpi1.max(), +1)
        np.testing.assert_almost_equal(Mpi1.min(), 0)
         
        self.solve_from_start(R_order, Mpi1,
                              ndim=ndim, num_iterations=num_iterations,
                              phase='pi1')
        self.solve_from_start(R_order, Mpi2,
                              ndim=ndim, num_iterations=num_iterations,
                              phase='pi2')

        # Choose the best one 
        measure = 'robust'
        best_iteration = self.get_best_so_far(measure) 
        self.iteration(best_iteration)
        phase = best_iteration['phase']
        
        if warp:
            self.warp(ndim, best_iteration['S'],
                  min_ratio=0.25, divisions=25, depths=1, phase=phase)
    
            best_iteration = self.get_best_so_far(measure)
             
            self.iteration(best_iteration)
    
    def get_best_so_far(self, measure='spearman', measure_sign= -1):
        all_spearman = list(x[measure] for x in self.iterations)
        best_scores = np.argsort(measure_sign * np.array(all_spearman))
        best_iteration = self.iterations[best_scores[0]] 
        print('Best so far: #%d (according to %s %d)' % 
              (best_scores[0], measure, measure_sign))
        return best_iteration

    def solve_from_start(self, R_order, M0, ndim, num_iterations, phase):
        current_guess_for_S = best_embedding_on_sphere(M0, ndim)

        for iteration in range(num_iterations): #@UnusedVariable
            guess_for_C = cosines_from_directions(current_guess_for_S)
            guess_for_C_sorted = np.sort(guess_for_C.flat)
            new_estimated_C = guess_for_C_sorted[R_order]
            new_guess_for_S = best_embedding_on_sphere(new_estimated_C, ndim) 
            
            data = dict(S=new_guess_for_S, phase=phase)
            self.iteration(data)
            
            current_guess_for_S = new_guess_for_S 

    def warp(self, ndim, base_S, min_ratio=0.25, divisions=10, depths=2, phase=None):
        base_D = distances_from_directions(base_S)
        
        diameter = base_D.max()
        max_ratio = np.pi / diameter
        print('Detected max D = %f, max ratio = %f' % (diameter, max_ratio))
        
        def guess_for_ratio(ratio):
            Cwarp = cosines_from_distances(base_D * ratio)
            return best_embedding_on_sphere(Cwarp, ndim)
   
        for depth in range(depths):
            ratios = np.exp(np.linspace(np.log(min_ratio), np.log(max_ratio), divisions))
            ratios = np.array(sorted(ratios.tolist() + [1.0])) # always include 1.0 
            print('Depth %d/%d: ratios: %f to %f' % (depth, depths, ratios[0], ratios[-1]))

            scores = []
            for i, ratio in enumerate(ratios):
                new_guess_for_S = guess_for_ratio(ratio)
                data = dict(S=new_guess_for_S, phase=phase)
                self.iteration(data)
                score = self.iterations[-1]['spearman']
                scores.append(score)
                
            print('Scores: %s' % list(scores))
            scores = np.array(scores)
            best_two = np.argsort(-scores)[:2]
            lower = min(best_two)
            upper = max(best_two)
            assert (upper >= scores[upper:]).all()
            assert (lower >= scores[:lower]).all()
#            lower = max(0, lower - 1)
#            upper = min(upper + 1, len(scores) - 1)
#            
#            print('lower: %d upper: %d' % (lower, upper))
            min_ratio = ratios[lower]
            max_ratio = ratios[upper]


