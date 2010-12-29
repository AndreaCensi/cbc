import numpy as np
from types import FunctionType

from . import CalibAlgorithm

from ..tools  import (scale_score, best_embedding_on_sphere,
                      directions_to_cosines,
                      angles_to_directions, normalize_pi, \
                      directions_to_angles)
from snp_geometry.utils import assert_allclose



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
            guess_for_C = directions_to_cosines(current_guess_for_S)
            guess_for_C_sorted = np.sort(guess_for_C.flat)
            new_estimated_C = guess_for_C_sorted[R_order]
            new_guess_for_S = best_embedding_on_sphere(new_estimated_C, ndim) 
            
            data = dict(S=new_guess_for_S, **locals())
            self.iteration(data)
            
            current_guess_for_S = new_guess_for_S
            if self.seems_to_have_converged():
                break



class CBCa(CBC):
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
            guess_for_C = directions_to_cosines(current_guess_for_S)
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
        base_C = directions_to_cosines(base_S)
        base_D = np.arccos(base_C)
        
        max_ratio = np.pi * 2 / self.iterations[-1]['diameter']
        print('Detected max D = %f, max ratio = %f' % (base_D.max(), max_ratio))
        
        def guess_for_ratio(ratio):
            angles = directions_to_angles(base_S)
            x = base_S[0, :].mean()
            y = base_S[1, :].mean()
            center = np.arctan2(y, x)
            differences = normalize_pi(angles - center)
            
            new_angles = center + differences * ratio
            return angles_to_directions(new_angles)
        
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
