from . import CalibAlgorithm, np, EUCLIDEAN
from ..tools import random_rotation


class Cheater(CalibAlgorithm):
    ''' This is used for debugging. It cheats by
        looking at the ground truth and applies a random rotation. '''

    def _solve(self, R): #@UnusedVariable
        if self.true_S is not None:
            # TODO: add general orthogonal transform
            ndim = self.true_S.shape[0]
            if False: # useful for testing error estimation procedures 
                R = random_rotation(ndim)
                guess = np.dot(R, self.true_S)
            guess = self.true_S
        else:
            assert False

        results = dict(S=guess)
        self.iteration(results)


class EuclideanCheater(CalibAlgorithm):
    def __init__(self, params):
        CalibAlgorithm.__init__(self, params, geometry=EUCLIDEAN)

    def _solve(self, R): #@UnusedVariable
        if self.true_S is not None:
            # TODO: add general orthogonal transform
            ndim = self.true_S.shape[0]
            R = random_rotation(ndim)
            guess = np.dot(R, self.true_S)
        else:
            assert False

        results = dict(S=guess)
        self.iteration(results)
