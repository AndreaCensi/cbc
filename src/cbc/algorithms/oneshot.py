from ..tools  import best_embedding_on_sphere    

from . import CalibAlgorithm


class OneShotEmbedding(CalibAlgorithm):
    
    def _solve(self, R):
        ndim = self.params['ndim']
        S = best_embedding_on_sphere(R, ndim)
        self.iteration(dict(S=S))

