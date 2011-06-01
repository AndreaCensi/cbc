
from .base import *
from .cbc import *
from .cheat import *
from .spherical_mds import *
from .classic_mds import *
from .random import *
from .cbc_robust import *
from .mds_robust import *

def get_list_of_algorithms_rss():
    return dict([
            ('cheat', (Cheater, {'ndim': 2})),
            ('rand2d', (Random, {'ndim': 2})),
            ('rand3d', (Random, {'ndim': 3})),
            ('embed2', (SphericalMDS, {'ndim': 2})),
            ('embed3', (SphericalMDS, {'ndim': 3})),
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
    
def get_list_of_algorithms():
    nit = 4
    return dict([
        ('cheat', (Cheater, {'ndim': 2})),
        ('echeat', (EuclideanCheater, {})),
        ('rand2d', (Random, {'ndim': 2})),
        ('rand3d', (Random, {'ndim': 3})),
        ('embed2', (SphericalMDS, {'ndim': 2})),
        ('embed3', (SphericalMDS, {'ndim': 3})),
        ('emds2', (EuclideanMDS, {'ndim': 2})),
        ('emds3', (EuclideanMDS, {'ndim': 3})),
        ('eCBC2d', (MDS_robust, dict(ndim=2, num_iterations=nit * 3, trust_top_perc=100))),
        ('eCBC2dr10', (MDS_robust, dict(ndim=2, num_iterations=nit * 3, trust_top_perc=10))),
        ('eCBC2dr50', (MDS_robust, dict(ndim=2, num_iterations=nit * 3, trust_top_perc=50))),
        ('eCBC2dr80', (MDS_robust, dict(ndim=2, num_iterations=nit * 3, trust_top_perc=80))),
        
        ('CBC2d', (CBCchoose, {'ndim': 2, 'num_iterations': nit, 'warp': False})),
        ('CBC3d', (CBCchoose, {'ndim': 3, 'num_iterations': nit, 'warp': False})),
        ('CBC2dr50', (CBC_robust, {'ndim': 2, 'num_iterations': nit, 'warp': False,
                                    'trust_top_perc': 50})),
        ('CBC3dr50', (CBC_robust, {'ndim': 3, 'num_iterations': nit, 'warp': False,
                                    'trust_top_perc': 50})),

        ('CBC3dw', (CBCchoose, {'ndim': 3, 'num_iterations': nit, 'warp': True})),
        ('CBC3dr50w', (CBC_robust, {'ndim': 3, 'num_iterations': nit, 'warp': True,
                                    'trust_top_perc': 50})),
        ('CBC2dw', (CBCchoose, {'ndim': 2, 'num_iterations': nit, 'warp': True})),
        ('CBC2dr50w', (CBC_robust, {'ndim': 2, 'num_iterations': nit, 'warp': True,
                                    'trust_top_perc': 50})),
        

        ('CBC2dr10', (CBC_robust, {'ndim': 2, 'num_iterations': nit, 'warp': False,
                                    'trust_top_perc': 10})),
        ('CBC2dr10w', (CBC_robust, {'ndim': 2, 'num_iterations': nit, 'warp': True,
                                    'trust_top_perc': 10})),
        ])
    
