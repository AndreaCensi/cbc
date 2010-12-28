
from .base import *
from .cbc import *
from .cbct import *
from .cbct2 import *
from .cheat import *
from .oneshot import *
from .random import *


def get_list_of_algorithms():
    its = 6
    return dict([
            ('cheat', (Cheater, {'ndim': 2})) ,
            ('rand', (Random, {'ndim': 2})),
            ('cbct2', (CBCt2, {'ndim': 2, 'num_iterations': 10})),
            ('cbc75', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 75})),
            ('cbc50', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 50})),
            ('cbc20', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 20})),
            ('cbc5', (CBCt, {'ndim': 2, 'num_iterations': its, 'trust_R_top_perc': 10})),
            ('cbc', (CBC, {'ndim': 2, 'num_iterations': its})),
            ('embed2', (OneShotEmbedding, {'ndim': 2})),
        ])
    
    
