from . import (CBC_robust, Cheater, EuclideanCheater, MDS_robust, Random,
    SphericalMDS, EuclideanMDS, CBCchoose)


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
        ('eCBC2d', (MDS_robust, dict(ndim=2, num_iterations=nit * 3,
                                      trust_top_perc=100))),
        ('eCBC2dr10', (MDS_robust, dict(ndim=2, num_iterations=nit * 3,
                                        trust_top_perc=10))),
        ('eCBC2dr50', (MDS_robust, dict(ndim=2, num_iterations=nit * 3,
                                        trust_top_perc=50))),
        ('eCBC2dr80', (MDS_robust, dict(ndim=2, num_iterations=nit * 3,
                                        trust_top_perc=80))),

        ('CBC2d', (CBCchoose, {'ndim': 2, 'num_iterations': nit, 'warp': False,
                               'measure': 'spearman'})),
        ('CBC3d', (CBCchoose, {'ndim': 3, 'num_iterations': nit, 'warp': False,
                               'measure': 'spearman'})),
        ('CBC2dr50', (CBC_robust, {'ndim': 2, 'num_iterations': nit,
                                   'warp': False,
                                    'trust_top_perc': 50,
                                    'measure': 'spearman_robust'})),
        ('CBC3dr50', (CBC_robust, {'ndim': 3, 'num_iterations': nit,
                                   'warp': False,
                                    'trust_top_perc': 50,
                                    'measure': 'spearman_robust'})),

            ('CBC3dr50w', (CBC_robust, {'ndim': 3, 'num_iterations': nit,
                                        'warp': True,
                                        'trust_top_perc': 50,
                                        'measure': 'spearman_robust'})),
            ('CBC3dr10w', (CBC_robust, {'ndim': 3, 'num_iterations': nit,
                                        'warp': True,
                                        'trust_top_perc': 10,
                                        'measure': 'spearman_robust'})),

        ('CBC3dw', (CBCchoose, {'ndim': 3,
                                'num_iterations': nit,
                                'warp': True,
                                'measure': 'spearman'
                                })),
        ('CBC3dr50w', (CBC_robust, {'ndim': 3, 'num_iterations': nit,
                                    'warp': True,
                                    'trust_top_perc': 50,
                                    'measure': 'spearman_robust'})),
        ('CBC2dw', (CBCchoose, {'ndim': 2, 'num_iterations': nit, 'warp': True,
                                'measure': 'spearman'})),
        ('CBC2dr50w', (CBC_robust, {'ndim': 2, 'num_iterations': nit,
                                    'warp': True,
                                    'trust_top_perc': 50,
                                    'measure': 'spearman_robust'})
                        ),


        ('CBC2dr10', (CBC_robust, {'ndim': 2, 'num_iterations': nit,
                                    'warp': False,
                                    'trust_top_perc': 10,
                                    'measure': 'spearman_robust'})),
        ('CBC2dr10w', (CBC_robust, {'ndim': 2, 'num_iterations': nit,
                                     'warp': True,
                                    'trust_top_perc': 10,
                                    'measure': 'spearman_robust'})),

        ('CBC3dr50w_pi2', (CBC_robust, {'ndim': 3, 'num_iterations': 30,
                                        'warp': True,
                                        'trust_top_perc': 50, 'starting': [2],
                                        'measure': 'spearman_robust'})),

        ('CBC3dw_15', (CBCchoose, {'ndim': 3, 'num_iterations': 15,
                                    'warp': True,
                                    'measure': 'spearman'})),

        ('CBC_quick', (CBC_robust, {'ndim': 3, 'num_iterations': 15,
                                    'warp': True, 'starting': [1],
                                    'trust_top_perc': 40,
                                    'measure': 'spearman'}))

        ])

