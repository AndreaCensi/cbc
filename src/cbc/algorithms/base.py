import numpy as np

from contracts import check_multiple, check

from ..tools import (find_best_orthogonal_transform,
                    overlap_error_after_orthogonal_transform,
                    get_cosine_matrix_from_s,
                    get_distance_matrix_from_cosine,
                    compute_relative_error, scale_score, compute_diameter,
                    correlation_coefficient, directions_to_angles,
                    find_closest_multiple)

class CalibAlgorithm(object):
    
    def __init__(self, params):
        self.params = params
    
    def solve(self, R, true_S=None):
        self.R = R
        self.R_order = scale_score(self.R)
        self.iterations = []
        self.true_S = true_S
        if true_S is not None:
            check('directions', true_S)
        self._solve(R)
        self.n = R.shape[0]
        
        last_iteration = self.iterations[-1]
        results = {}
        copy_fields = ['rel_error' , 'rel_error_deg', 'spearman', 'spearman_robust',
                       'error', 'error_deg', 'S', 'S_aligned', 'diameter',
                       'diameter_deg', 'angles_corr']
        for f in copy_fields:
            results[f] = last_iteration[f]
        
        results['R'] = R    
        results['n'] = R.shape[0]
        results['params'] = self.params
        results['true_S'] = true_S
        

        if true_S is not None:
            results['true_C'] = get_cosine_matrix_from_s(true_S)
            results['true_dist'] = \
                get_distance_matrix_from_cosine(results['true_C'])
            
        results['iterations'] = self.iterations
            
        self.results = results
        return self.results
    
    def iteration(self, data):
        for x in ['self']: 
            if x in data: del data[x]
        
        S = data['S']
        check_multiple([('array[NxN]', self.R), ('array[*xN]', S)])
            
        check('directions', S)
            
        # compute measures here
        if self.true_S is not None:
            
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


            # Observable error
            C = get_cosine_matrix_from_s(S)
            C_order = scale_score(C)
            data['spearman'] = correlation_coefficient(C_order, self.R_order)
#            data['spearman_robust'] = np.abs(C_order - self.R_order).mean() 
            data['spearman_robust'] = np.abs((C_order - self.R_order) * C_order).mean() 
            
            data['diameter'] = compute_diameter(S)
            data['diameter_deg'] = np.degrees(data['diameter'])
            
            true_angles_deg = np.degrees(directions_to_angles(self.true_S))
            angles_deg = np.degrees(directions_to_angles(S))
            angles_deg = find_closest_multiple(angles_deg, true_angles_deg, 360)
            data['angles_corr'] = correlation_coefficient(true_angles_deg, angles_deg)
            
            def varstat(x, format='%.3f'):
                label = x
#                if label.endswith('_deg'):
#                    label = label[:-len('_deg')]
                label = x[:5]
                current = data[x]
                s = ' %s: %s' % (label, format % current)
                
                if self.iterations:
                    previous = self.iterations[-1][x]
                    sign = '+' if current > previous else '-'
                    s += ' %s' % sign
                return s
            
            status = ('It: %d' % len(self.iterations) + 
                      varstat('diameter_deg', '%d') + 
                      varstat('spearman', '%.8f') + 
                      varstat('spearman_robust', '%.8f') + 
                      varstat('error_deg', '%.3f') + 
                      varstat('rel_error_deg', '%.3f') + 
                      varstat('angles_corr', '%.8f'))
            print status
        else:
            print('Iteration %3d' % len(self.iterations))
            
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
        

    def param(self, name, value, desc=None):
        self.params[name] = value
        
    def __str__(self):
        params = "-".join('%s=%s' % (k, v) for k, v in self.params.items()) 
        return '%s(%s)' % (self.__class__.__name__, params)
            
