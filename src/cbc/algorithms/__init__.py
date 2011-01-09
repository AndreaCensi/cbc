
from .base import *
from .cbc import *
from .cheat import *
from .oneshot import *
from .random import *
from .cbc_robust import *


def get_list_of_algorithms():
    return dict([
            ('cheat', (Cheater, {'ndim': 2})),
            ('rand2d', (Random, {'ndim': 2})),
            ('rand3d', (Random, {'ndim': 3})),
            ('embed2', (OneShotEmbedding, {'ndim': 2})),
            ('embed3', (OneShotEmbedding, {'ndim': 3})),
            ('CBC2d', (CBCchoose, {'ndim': 2, 'num_iterations': 7, 'warp': False})),
            ('CBC3d', (CBCchoose, {'ndim': 3, 'num_iterations': 7, 'warp': False})),
            ('CBC2dr50', (CBC_robust, {'ndim': 2, 'num_iterations': 7, 'warp': False,
                                        'trust_top_perc': 50})),
            ('CBC3dr50', (CBC_robust, {'ndim': 3, 'num_iterations': 7, 'warp': False,
                                        'trust_top_perc': 50})),

            ('CBC3dw', (CBCchoose, {'ndim': 3, 'num_iterations': 7, 'warp': True})),
            ('CBC3dr50w', (CBC_robust, {'ndim': 3, 'num_iterations': 7, 'warp': True,
                                        'trust_top_perc': 50})),
            ('CBC2dw', (CBCchoose, {'ndim': 2, 'num_iterations': 7, 'warp': True})),
            ('CBC2dr50w', (CBC_robust, {'ndim': 2, 'num_iterations': 7, 'warp': True,
                                        'trust_top_perc': 50})),
            

            ('CBC2dr10', (CBC_robust, {'ndim': 2, 'num_iterations': 7, 'warp': False,
                                        'trust_top_perc': 10})),
            ('CBC2dr10w', (CBC_robust, {'ndim': 2, 'num_iterations': 7, 'warp': True,
                                        'trust_top_perc': 10})),
        ])
    
    
