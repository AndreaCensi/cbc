import numpy as np

from contracts import check_multiple, check

from ..tools import (find_best_orthogonal_transform,
                    overlap_error_after_orthogonal_transform,
                    get_cosine_matrix_from_s,
                    get_distance_matrix_from_cosine,
                    compute_relative_error)

class CalibAlgorithm(object):
    
    def __init__(self, params):
        self.params = params
    
    def solve(self, R, true_S=None):
        self.R = R
        self.iterations = []
        self.true_S = true_S
        if true_S is not None:
            check('directions', true_S)
        self._solve(R)
        self.n = R.shape[0]
        
        last_iteration = self.iterations[-1]
        results = {}
        copy_fields = ['rel_error' , 'rel_error_deg',
                       'error', 'error_deg', 'S', 'S_aligned']
        for f in copy_fields:
            results[f] = last_iteration[f]
        
        results['R'] = R    
        results['n'] = R.shape[0]
        results['params'] = self.params
        results['true_S'] = true_S
        if true_S is not None:
            results['true_C'] = get_cosine_matrix_from_s(true_S)
            results['true_dist'] = get_distance_matrix_from_cosine(results['true_C'])
            
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
            
            print('Iteration %d: error %.3f  relative %.3f ' % 
                  (len(self.iterations), data['error_deg'], data['rel_error_deg']))
        else:
            print('Iteration %d' % len(self.iterations))
            
        self.iterations.append(data)

    def param(self, name, value, desc=None):
        self.params[name] = value
        
    def __str__(self):
        params = "-".join('%s=%s' % (k, v) for k, v in self.params.items()) 
        return '%s(%s)' % (self.__class__.__name__, params)
            
