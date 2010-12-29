
from .base import *
from .cbc import *
from .cbct import *
from .cbct2 import *
from .cheat import *
from .oneshot import *
from .random import *


def get_list_of_algorithms():
    its = 20
    return dict([
            ('cheat', (Cheater, {'ndim': 2})) ,
            ('rand', (Random, {'ndim': 2})),
            ('cbct2', (CBCt2, {'ndim': 2, 'num_iterations': 10})),
            ('cbc_t75', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 75})),
            ('cbc_t50', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 50})),
            ('cbc_t20', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 20})),
            ('cbc_t10', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 10})),
            ('cbc', (CBC, {'ndim': 2, 'pie': 2, 'num_iterations': its})),
            ('cbc1pi', (CBC, {'pie':1, 'ndim': 2, 'num_iterations': its})),
            ('cbc2pi', (CBC, {'pie':2, 'ndim': 2, 'num_iterations': its})),
            ('cbc2pia', (CBCa, {'pie':2, 'ndim': 2, 'num_iterations': 5,
                                'num_extra_iterations': 15})),
            ('embed2', (OneShotEmbedding, {'ndim': 2})),
        ])
    
    
