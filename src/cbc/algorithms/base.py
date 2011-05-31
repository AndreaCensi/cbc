import numpy as np

from contracts import check_multiple, check

from ..tools import (find_best_orthogonal_transform,
                     overlap_error_after_orthogonal_transform,
                     scale_score, compute_diameter,
                     correlation_coefficient, compute_relative_error,
                     find_closest_multiple, angles_from_directions,
                     distances_from_cosines, cosines_from_directions,
                     euclidean_distances,
                     mean_euclidean_distance_after_orthogonal_transform)


SPHERICAL = 'S'
EUCLIDEAN = 'E'
GEOMETRIES = [SPHERICAL, EUCLIDEAN]
    
    
class CalibAlgorithm(object):
    
    def __init__(self, params, geometry=SPHERICAL):
        self.params = params
        assert geometry in GEOMETRIES
        self.geometry = geometry
    
    def is_spherical(self):
        return self.geometry == SPHERICAL
    
    def is_euclidean(self):
        return self.geometry == EUCLIDEAN   
    
    def solve(self, R, true_S=None):
        self.R = R
        self.R_order = scale_score(self.R).astype('int32')
        self.R_sorted = np.sort(R.flat)
        
        self.n = R.shape[0]
        
        self.iterations = []
        self.true_S = true_S
        
        if self.is_spherical():
            if true_S is not None:
                check('directions', true_S)
        
        self._solve(R)
        
        for it in self.iterations:
            if 'C' in it:
                del it['C']
                
        last_iteration = self.iterations[-1]
        results = {}
        copy_fields = ['rel_error' , 'rel_error_deg', 'spearman', 'spearman_robust',
                       'error', 'error_deg', 'S', 'S_aligned', 'diameter',
                       'diameter_deg', 'angles_corr', 'deriv_sign', 'phase',
                       'scaled_error', 'scaled_rel_error']
        for f in copy_fields:
            if f in last_iteration:
                results[f] = last_iteration[f]
        
        results['R'] = R
        results['R_order'] = scale_score(R)        
        results['n'] = R.shape[0]
        results['params'] = self.params
        results['true_S'] = true_S
        
        if self.is_spherical():
            if true_S is not None:
                results['true_C'] = cosines_from_directions(true_S)
                results['true_dist'] = distances_from_cosines(results['true_C'])
                
        results['iterations'] = self.iterations
        results['geometry'] = self.geometry
        self.results = results
        return self.results
    
    def iteration(self, data):
        """ Records one iteration of the algorithm """
        
        for x in ['self']: 
            if x in data: del data[x]
        
        S = data['S']
        check_multiple([('array[NxN]', self.R), ('array[*xN]', S)])
            
        if self.is_spherical():
            check('directions', S)
            
            # Observable errors
            C = cosines_from_directions(S)
            C_order = scale_score(C)
            data['spearman'] = correlation_coefficient(C_order, self.R_order)

            # data['RCorder_diff'] = np.abs(C_order - self.R_order).sum() / C_order.size
        
            valid = self.R_order > self.R.size * 0.6
            data['spearman_robust'] = correlation_coefficient(C_order[valid],
                                                          self.R_order[valid])
                     
            data['diameter'] = compute_diameter(S)
            data['diameter_deg'] = np.degrees(data['diameter'])
        
        if self.is_euclidean():
            D = euclidean_distances(S)
            D_order = scale_score(D)
            data['spearman'] = correlation_coefficient(-D_order, self.R_order)
            valid = self.R_order > self.R.size * 0.6
            data['spearman_robust'] = correlation_coefficient(-D_order[valid],
                                                          self.R_order[valid])

        
        data['robust'] = data['spearman_robust']
        
        # These are unobservable statistics
        if self.is_spherical() and self.true_S is not None:
            # add more rows to S if necessary
            K = S.shape[0]
            if K != self.true_S.shape[0]:
                newS = np.zeros(self.true_S.shape)
                newS[:K, :] = S
                newS[K:, :] = 0
                S = newS
                check('directions', S)

            Rest = find_best_orthogonal_transform(S, self.true_S)
            data['S_aligned'] = np.dot(Rest, S)
            data['error'] = \
                overlap_error_after_orthogonal_transform(S, self.true_S)
            data['error_deg'] = np.degrees(data['error'])            
            data['rel_error'] = compute_relative_error(self.true_S, S, 10)
            data['rel_error_deg'] = np.degrees(data['rel_error'])

            # only valid in 2d
            if K == 2:
                true_angles_deg = np.degrees(angles_from_directions(self.true_S))
                angles_deg = np.degrees(angles_from_directions(data['S_aligned']))
                angles_deg = find_closest_multiple(angles_deg, true_angles_deg, 360)
                data['angles_corr'] = correlation_coefficient(true_angles_deg, angles_deg)
            
        if self.is_euclidean() and self.true_S is not None:
            D = euclidean_distances(S)
            true_D = euclidean_distances(self.true_S)
            
            rel_error = np.abs(D - true_D).mean()
            data['rel_error'] = rel_error 

            scale = true_D.mean() / D.mean()  
            scaled_rel_error = np.abs(D * scale - true_D).mean()
            data['scaled_rel_error'] = scaled_rel_error
            
            scaled_S = scale * S 
            def remove_mean(x):
                k, n = x.shape
                m = np.tile(x.mean(axis=1).reshape((k, 1)), (1, n))
                assert m.shape == x.shape
                return x - m
            
            trans_scaled_S = remove_mean(scaled_S)
            trans_true_S = remove_mean(self.true_S)
            data['scaled_error'] = \
                mean_euclidean_distance_after_orthogonal_transform(
                            trans_scaled_S, trans_true_S)
           
            
        def varstat(x, format='%.3f', label=None, sign= +1):
            if label is None: label = x[:5]
            if not x in data: return ' %s: /' % label
            current = data[x]
            s = ' %s: %s' % (label, format % current)
            
            if self.iterations:
                all_previous = np.array([it[x] for it in self.iterations])
                
                previous = all_previous[-1]
                is_best = sign * current >= max(sign * all_previous)
                if is_best:
                    mark = 'B'
                else:
                    mark = '+' if sign * current > sign * previous else '-'
                s += ' %s' % mark
            return s
            
        status = ('It: %2d' % len(self.iterations) + 
                  varstat('diameter_deg', '%3d') + 
                  varstat('spearman', '%.8f', label='spear') + 
                  varstat('spearman_robust', '%.8f', label='sp_rob'))
        
        if self.is_spherical():
            status += (varstat('error_deg', '%5.3f', sign= -1) + 
                      varstat('rel_error_deg', '%5.3f', sign= -1))
        if self.is_euclidean():
            status += (varstat('scaled_error', '%5.3f', sign= -1, label='s_err') + 
                      varstat('scaled_rel_error', '%5.3f', sign= -1, label='s_r_err'))
            
#                  varstat('Ddist', '%.5f', label='Ddist', sign= -1)    
#                  varstat('RCorder_diff', '%.3f', label='RCorder')  
#                  varstat('angles_corr', '%.8f')  
                  
        print(status)
            
        self.iterations.append(data)
        
    def seems_to_have_converged(self, min_ratio=0.1):
        if len(self.iterations) < 3:
            return False
        last = [ self.iterations[i]['spearman'] for i in [-3, -2, -1]]
        delta1 = last[-3] - last[-2]
        delta2 = last[-2] - last[-1]
        ratio = delta2 / delta1
        print('Convergence guess: ratio = %f' % ratio)
        if ratio < min_ratio and len(self.iterations) > 5:
            return True
        else:
            return False
        

    def param(self, name, value, desc=None): #@UnusedVariable XXX:
        self.params[name] = value
        
    def __str__(self):
        params = "-".join('%s=%s' % (k, v) for k, v in self.params.items()) 
        return '%s(%s)' % (self.__class__.__name__, params)
            
