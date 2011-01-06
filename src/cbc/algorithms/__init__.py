
from .base import *
from .cbc import *
from .cbct import *
from .cbct2 import *
from .cheat import *
from .oneshot import *
from .random import *
from .cbc_robust import *


def get_list_of_algorithms():
    its = 20
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
#            
#            
#            ('rand', (Random, {'ndim': 2})),
#            ('CBCb', (CBCchoose, {'ndim': 2, 'num_iterations': 5, 'warp': True})),
#            ('CBCb3', (CBCchoose, {'ndim': 3, 'num_iterations': 3, 'warp': False})),
#
#            
#            ('CBCr20', (CBC_robust, {'ndim': 2, 'num_iterations': 10, 'warp': False,
#                                        'trust_top_perc': 20})),
#            ('CBCr50', (CBC_robust, {'ndim': 2, 'num_iterations': 10, 'warp': False,
#                                        'trust_top_perc': 50})),
#            ('CBCr70', (CBC_robust, {'ndim': 2, 'num_iterations': 10, 'warp': False,
#                                        'trust_top_perc': 70})),
#                                        
#            ('cbct2', (CBCt2, {'ndim': 2, 'num_iterations': 10})),
#            ('cbc_t75', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 75})),
#            ('cbc_t50', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 50})),
#            ('cbc_t20', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 20})),
#            ('cbc_t10', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 10})),
#            
#            ('cbc', (CBC, {'ndim': 2, 'pie': 2, 'num_iterations': its})),
#            ('cbc1pi', (CBC, {'pie':1, 'ndim': 2, 'num_iterations': its})),
#            ('cbc2pi', (CBC, {'pie':2, 'ndim': 2, 'num_iterations': its})),
#            ('cbc1pia', (CBCa, {'pie':1, 'ndim': 2, 'num_iterations': 5,
#                                'num_extra_iterations': 15})),
#            ('cbc2pia', (CBCa, {'pie':2, 'ndim': 2, 'num_iterations': 5,
#                                'num_extra_iterations': 15})),
#            ('cbc2pi1', (CBC, {'pie':2, 'ndim': 2, 'num_iterations': 1})),
        
        ])
    
    
