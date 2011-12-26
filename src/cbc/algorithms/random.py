from . import CalibAlgorithm, np
from ..tools import project_vectors_onto_sphere


class Random(CalibAlgorithm):
    ''' This is used for debugging. Provides a random guess. '''

    def _solve(self, R):
        ndim = self.params['ndim']
        N = R.shape[0]
        X = np.random.randn(ndim, N)
        guess = project_vectors_onto_sphere(X)
        self.iteration(dict(S=guess))
