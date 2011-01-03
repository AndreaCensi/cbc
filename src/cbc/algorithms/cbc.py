import numpy as np
from types import FunctionType

from . import CalibAlgorithm

from ..tools  import (scale_score, best_embedding_on_sphere,
                      cosines_from_directions,
                      directions_from_angles,
                      normalize_pi,
                      distances_from_directions,
                      angles_from_directions,
                      cosines_from_distances)

from snp_geometry import assert_allclose 




class CBC(CalibAlgorithm):
    def _solve(self, R):
        ndim = self.params['ndim']
        num_iterations = self.params['num_iterations']
        pie = self.params['pie']
        
        # Score of each datum -- must be computed only once
        R_order = scale_score(R).astype('int32')

        M = (R_order * 2.0 / (R.size - 1)) - 1
        np.testing.assert_almost_equal(M.max(), +1)
        np.testing.assert_almost_equal(M.min(), -1)
        if pie == 1:
            M = (M + 1) / 2
        elif pie == 2:
            pass
        else:
            assert False
            
        current_guess_for_S = best_embedding_on_sphere(M, ndim)

        for iteration in range(num_iterations):
            guess_for_C = cosines_from_directions(current_guess_for_S)
            guess_for_C_sorted = np.sort(guess_for_C.flat)
            new_estimated_C = guess_for_C_sorted[R_order]
            new_guess_for_S = best_embedding_on_sphere(new_estimated_C, ndim) 
            
            data = dict(S=new_guess_for_S, **locals())
            self.iteration(data)
            
            current_guess_for_S = new_guess_for_S
            if self.seems_to_have_converged():
                break


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
                              ndim=ndim, num_iterations=num_iterations)
        self.solve_from_start(R_order, Mpi2,
                              ndim=ndim, num_iterations=num_iterations)

        # Choose the best one
        self.get_best_so_far('spearman_robust')
        best_iteration = self.get_best_so_far() 
        self.iteration(best_iteration)
        
        if warp:
            self.warp(ndim, best_iteration['S'],
                  min_ratio=0.25, divisions=15, depths=1)
    
            self.get_best_so_far('spearman_robust')
            best_iteration = self.get_best_so_far() 
            self.iteration(best_iteration)
    
    def get_best_so_far(self, measure='spearman', measure_sign= -1):
        all_spearman = list(x[measure] for x in self.iterations)
        best_scores = np.argsort(measure_sign * np.array(all_spearman))
        best_iteration = self.iterations[best_scores[0]] 
        print('Best so far: #%d (according to %s %d)' % 
              (best_scores[0], measure, measure_sign))
        return best_iteration

    def solve_from_start(self, R_order, M0, ndim, num_iterations):
        current_guess_for_S = best_embedding_on_sphere(M0, ndim)

        for iteration in range(num_iterations):
            guess_for_C = cosines_from_directions(current_guess_for_S)
            guess_for_C_sorted = np.sort(guess_for_C.flat)
            new_estimated_C = guess_for_C_sorted[R_order]
            new_guess_for_S = best_embedding_on_sphere(new_estimated_C, ndim) 
            
            data = dict(S=new_guess_for_S, **locals())
            self.iteration(data)
            
            current_guess_for_S = new_guess_for_S
#            if self.seems_to_have_converged():
#                break

    def warp(self, ndim, base_S, min_ratio=0.25, divisions=10, depths=2):
        base_D = distances_from_directions(base_S)
        
        diameter = base_D.max()
        max_ratio = np.pi / diameter
        print('Detected max D = %f, max ratio = %f' % (diameter, max_ratio))
        
        def guess_for_ratio(ratio):
            Cwarp = cosines_from_distances(base_D * ratio)
            return best_embedding_on_sphere(Cwarp, ndim)
   
        for depth in range(depths):
            ratios = np.exp(np.linspace(np.log(min_ratio), np.log(max_ratio), divisions))
            print('Depth %d/%d: ratios: %f to %f' % (depth, depths, ratios[0], ratios[-1]))

            scores = []
            for i, ratio in enumerate(ratios):
                new_guess_for_S = guess_for_ratio(ratio)
                data = dict(S=new_guess_for_S, **purify_locals(locals()))
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



class CBCa(CalibAlgorithm):
    def _solve(self, R):
        ndim = self.params['ndim']
        num_iterations = self.params['num_iterations']
        pie = self.params['pie']
        
        # Score of each datum -- must be computed only once
        R_order = scale_score(R).astype('int32')

        M = (R_order * 2.0 / (R.size - 1)) - 1
        np.testing.assert_almost_equal(M.max(), +1)
        np.testing.assert_almost_equal(M.min(), -1)
        if pie == 1:
            M = (M + 1) / 2
        elif pie == 2:
            pass
        else:
            assert False
            
        current_guess_for_S = best_embedding_on_sphere(M, ndim)

        for iteration in range(num_iterations):
            guess_for_C = cosines_from_directions(current_guess_for_S)
            guess_for_C_sorted = np.sort(guess_for_C.flat)
            new_estimated_C = guess_for_C_sorted[R_order]
            new_guess_for_S = best_embedding_on_sphere(new_estimated_C, ndim) 
            
            data = dict(S=new_guess_for_S, **locals())
            self.iteration(data)
            
            current_guess_for_S = new_guess_for_S

#        max_ratio = 2
        min_ratio = 0.25
        divisions = 10
        depths = 2
        base_S = current_guess_for_S.copy()
        base_C = cosines_from_directions(base_S)
        base_D = np.arccos(base_C)
        
        max_ratio = np.pi * 2 / self.iterations[-1]['diameter']
        print('Detected max D = %f, max ratio = %f' % (base_D.max(), max_ratio))
        
        def guess_for_ratio(ratio):
            angles = angles_from_directions(base_S)
            x = base_S[0, :].mean()
            y = base_S[1, :].mean()
            center = np.arctan2(y, x)
            differences = normalize_pi(angles - center)
            
            new_angles = center + differences * ratio
            return directions_from_angles(new_angles)
        
#            careful_C = distances_to_cosines(base_D * ratio)
#            S = best_embedding_on_sphere(careful_C, ndim)
#             
#            for a in range(3):
#                D = ratio * np.arccos(directions_to_cosines(S))
#                tmpC = np.sort(np.cos(D).flat)[R_order]
#                S = best_embedding_on_sphere(tmpC, ndim)             
#            return S 
            
        
        for depth in range(depths):
            print('min_ratio: %f max_ratio: %f' % (min_ratio, max_ratio))
            ratios = np.exp(np.linspace(np.log(min_ratio), np.log(max_ratio), divisions))
            print('Depth %d/%d: ratios: %f to %f' % (depth, depths, ratios[0], ratios[-1]))
            assert_allclose(ratios[0], min_ratio)
            assert_allclose(ratios[-1], max_ratio)
            
            scores = []
            for i, ratio in enumerate(ratios):
                new_guess_for_S = guess_for_ratio(ratio)
                data = dict(S=new_guess_for_S, **purify_locals(locals()))
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
            lower = max(0, lower - 1)
            upper = min(upper + 1, len(scores) - 1)
            
            print('lower: %d upper: %d' % (lower, upper))

            min_ratio = ratios[lower]
            max_ratio = ratios[upper]

        all_spearman = list(x['spearman'] for x in self.iterations)
        best_scores = np.argsort(-np.array(all_spearman))
        print('order spearman     : %s' % list(best_scores))
        all_spearman = list(x['spearman_robust'] for x in self.iterations)
        best_scores = np.argsort(+np.array(all_spearman))
        print('order spearman_rob : %s' % list(best_scores))
        
        self.iteration(self.iterations[best_scores[0]])

#        max_ratio = 2
#        min_ratio = 0.5
#        # divide in logarithmic intervals
#        n = 10
#        ratios = np.exp(np.linspace(np.log(min_ratio), np.log(max_ratio), n))
#        
#        base_S = current_guess_for_S.copy()
#        base_C = directions_to_cosines(base_S)
#        base_D = np.arccos(base_C)
#        for i, ratio in enumerate(ratios):
#            print('Ratio %d/%d %f' % (i, n, ratio))
#            careful_C = distances_to_cosines(base_D * ratio)
#            new_guess_for_S = best_embedding_on_sphere(careful_C, ndim) 
#
#            data = dict(S=new_guess_for_S, **locals())
#            self.iteration(data)

def purify_locals(l):
    l2 = dict(**l)
    for x in list(l.keys()):
        if x == 'self':
            del l2[x]
        if isinstance(l[x], FunctionType):
            del l2[x]
    return l2
