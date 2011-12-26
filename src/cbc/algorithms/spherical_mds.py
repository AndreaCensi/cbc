from . import CalibAlgorithm
from ..tools import best_embedding_on_sphere


class SphericalMDS(CalibAlgorithm):
    def _solve(self, R):
        ndim = self.params['ndim']
        S = best_embedding_on_sphere(R, ndim)
        self.iteration(dict(S=S))
