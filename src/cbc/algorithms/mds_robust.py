from . import CalibAlgorithm, np
from ..tools import scale_score, mds, euclidean_distances
from .base import EUCLIDEAN


class MDS_robust(CalibAlgorithm):

    def __init__(self, params):
        CalibAlgorithm.__init__(self, params, geometry=EUCLIDEAN)

    def _solve(self, R):
        ndim = self.params['ndim']
        num_iterations = self.params['num_iterations']
        trust_top_perc = self.params['trust_top_perc']

        # Score of each datum -- must be computed only once 
        R_order = scale_score(R).astype('int32')

#        D0 = R.max() - R 
        Mpi2 = (R_order * 2.0 / (R.size - 1)) - 1
        D0 = 1 - Mpi2
        for i in range(D0.shape[0]):
            D0[i, i] = 0

        np.testing.assert_almost_equal(D0.min(), 0)
        np.testing.assert_allclose(D0.diagonal(), 0)

        self.solve_from_start(R_order, D0,
                              ndim=ndim, num_iterations=num_iterations,
                              trust_top_perc=trust_top_perc,
                              phase='0')

#        measure = 'spearman_robust'
        measure = 'spearman'
        best_iteration = self.get_best_so_far(measure)
        self.iteration(best_iteration)

    def get_best_so_far(self, measure='spearman', measure_sign=(-1)):
        all_spearman = list(x[measure] for x in self.iterations)
        best_scores = np.argsort(measure_sign * np.array(all_spearman))
        best_iteration = self.iterations[best_scores[0]]
        print('Best so far: #%d (according to %s %d)' %
              (best_scores[0], measure, measure_sign))
        return best_iteration

    def solve_from_start(self, R_order, D0, ndim, num_iterations,
                         trust_top_perc, phase):
        current_guess_for_S = mds(D0, ndim)

        self.iteration(dict(S=current_guess_for_S, phase=phase))

        #R_percentile = R_order * 100.0 / R_order.size

        for iteration in range(num_iterations): #@UnusedVariable
            guess_for_D = euclidean_distances(current_guess_for_S)
            guess_for_D_sorted = -np.sort((-guess_for_D).flat)
            new_estimated_D = guess_for_D_sorted[R_order]

            if trust_top_perc != 100:
#                not_trusted = R_percentile < (100 - trust_top_perc)

                def percentile(X):
                    score = scale_score(X).astype('int32')
                    perc = score * 100.0 / X.size
                    return perc

                D_percentile = percentile(guess_for_D)
                not_trusted = D_percentile > (100 - trust_top_perc)

                new_estimated_D[not_trusted] = guess_for_D[not_trusted]
#                trusted = R_percentile >= (100 - trust_top_perc)
#                max_D = new_estimated_D[trusted].max()
#                max_D = new_estimated_D[not_trusted].min()
                num = not_trusted.sum()
                tot = not_trusted.size
                ratio = num * 1.0 / tot
                print('Ratio not trusted: %f (%d/%d)' % (ratio, num, tot))
#                old = guess_for_D[not_trusted]
#                new = new_estimated_D[not_trusted]
#                alpha = 0
#                new_estimated_D[not_trusted] = alpha * new + (1 - alpha) * old
#                print('maxD: %s' % max_D)

            new_guess_for_S = mds(new_estimated_D, ndim)

            data = dict(S=new_guess_for_S, phase=phase)
            self.iteration(data)

            current_guess_for_S = new_guess_for_S
