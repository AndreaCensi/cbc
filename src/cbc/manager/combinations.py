from collections import namedtuple

Combination = namedtuple('Combination', 'algorithms test_cases')

def get_list_of_combinations():
    combinations = {}
    combinations['all'] = Combination('*', '*')
    combinations['CBC'] = Combination(['cbc'], '*')
    combinations['CBC_vs_embed2'] = Combination(['cbc', 'embed2'], '*')
    combinations['CBCt'] = Combination('cbct*', '*') 
    combinations['tmp'] = Combination(['embed2', 'cbc'], ['fov135-identity'])
    combinations['tmp2'] = Combination(['cheat', #'rand',
                                        'embed2', 'cbc', 'cbct2'],
                                       ['fov135-linear01',
                                        'fov135-pow3_sat',
                                        'fov360-pow3_sat'])

    combinations['pow3'] = Combination(['cheat', #'rand',
                                        'embed2', 'cbc', 'cbct2'],
                                       ['fov135-pow3_sat',
                                        'fov180-pow3_sat',
                                        'fov225-pow3_sat',
                                        'fov360-pow3_sat'])
    
    combinations['tmp3'] = Combination(['cbc1pi', 'cbc2pi', 'embed2', 'cheat'],
                                       ['fov45-pow3_sat',
                                        'fov90-pow3_sat',
                                        'fov135-linear01',
                                        'fov270-linear01',
                                        'fov135-pow3_sat',
                                        'fov180-pow3_sat',
                                        'fov225-pow3_sat',
                                        'fov270-pow3_sat',
                                        'fov360-pow3_sat'])
    
    combinations['tmp4'] = Combination(['cbc2pia', 'embed2', 'cheat'],
                        ['fov135-pow3_sat', 'fov225-pow3_sat', 'fov270-pow3_sat']
                        + ['fov45-pow3_sat', 'fov90-pow3_sat'])

    combinations['tmp5'] = Combination(['cbc1pi', 'cbc2pi', 'cbc1pia', 'cbc2pia',
                                        'embed2', 'cheat'],
                                       ['fov45-pow3_sat',
                                        'fov90-pow3_sat',
                                        'fov135-linear01',
                                        'fov270-linear01',
                                        'fov135-pow3_sat',
                                        'fov180-pow3_sat',
                                        'fov225-pow3_sat',
                                        'fov270-pow3_sat',
                                        'fov360-pow3_sat'])
  
  
    combinations['CBCchoose'] = Combination(['CBCb', 'embed2', 'cheat'],
                                       ['fov45-pow3_sat',
                                        'fov45-linear01',
                                        'fov90-pow3_sat',
                                        'fov90-linear01',
                                        'fov180-pow3_sat',
                                        'fov180-linear01',
                                        'fov270-pow3_sat',
                                        'fov270-linear01'])

    combinations['CBCchoosedev'] = Combination(['CBCb'],
                                       ['fov180-pow3_sat',
                                        'fov270-pow3_sat'])
    
    combinations['real'] = Combination(['embed2', 'cheat', 'CBCb'],
                                            'sick_*')

    combinations['dev'] = Combination(['CBCr*', 'embed2', 'cheat', 'CBCb'],
                                        'sick_front-y')

    combinations['devreal'] = Combination(['CBCr*', 'embed2', 'cheat', 'CBCb'],
                                          'sick_*')

    paper_algos2d = ['cheat', 'rand2d', 'embed2', 'CBC2d', 'CBC2dr50']
    paper_algos2d += [ 'CBC2dw', 'CBC2dr50w']
    paper_algos3d = ['cheat', 'rand3d', 'embed3', 'CBC3d', 'CBC3dr50']
    paper_algos3d += [ 'CBC3dw', 'CBC3dr50w']

    addpost = lambda test_cases, suffix: [x + '-' + suffix for x in test_cases]
    
    observable2d = ['rand-2D-fov315-pow3_sat',
                    'rand-2D-fov315-pow7_sat',
                    'rand-2D-fov315-linear01',
                    'rand-2D-fov360-pow3_sat',
                    'rand-2D-fov360-pow7_sat',
                    'rand-2D-fov360-linear01']
    
    observable3d = ['rand-3D-fov45-pow3_sat',
                    'rand-3D-fov45-pow7_sat',
                    'rand-3D-fov45-linear01',
                    'rand-3D-fov90-pow3_sat',
                    'rand-3D-fov90-pow7_sat',
                    'rand-3D-fov90-linear01',
                    'rand-3D-fov270-pow3_sat',
                    'rand-3D-fov270-pow7_sat',
                    'rand-3D-fov270-linear01',
                    'rand-3D-fov360-pow3_sat',
                    'rand-3D-fov360-pow7_sat',
                    'rand-3D-fov360-linear01' 
                    ]
    
    unobservable2d = ['rand-2D-fov45-pow3_sat',
                      'rand-2D-fov45-pow7_sat',
                      'rand-2D-fov45-linear01',
                      'rand-2D-fov90-pow3_sat',
                      'rand-2D-fov90-pow7_sat',
                      'rand-2D-fov90-linear01']
    
    for t in ['noisy', 'zero']:
        combinations['paper-obs2d-%s' % t] = Combination(paper_algos2d, addpost(observable2d, t))
        ob3 = addpost(observable3d, t)
        if t == 'noisy':
            ob3.append('fly')
        combinations['paper-obs3d-%s' % t] = Combination(paper_algos3d, ob3)
        combinations['paper-unobs2d-%s' % t] = Combination(paper_algos2d, addpost(unobservable2d, t))
    
    paper_algos2d_sick = ['cheat', 'rand2d', 'embed2', 'CBC2d', 'CBC2dw',
                'CBC2dr10w', 'CBC2dr10']
    
    combinations['paper-sick'] = Combination(paper_algos2d_sick, 'sick_*')
                 
                 
    combinations['many'] = Combination(paper_algos3d,
                                       ['rand-3D-fov45-linear01-zero',
                                        'rand-3D-fov45-linear01-zero-many',
                                        'rand-3D-fov45-pow7_sat-zero',
                                        'rand-3D-fov45-pow7_sat-zero-many'])

    combinations['warp'] = Combination(
                    ['cheat', 'embed3', 'CBC3d', 'CBC3dr50', 'CBC3dw', 'CBC3dr50w' ],
            ['rand-3D-fov45-linear01-zero',
                                        'rand-3D-fov45-pow7_sat-zero'])

    
    combinations['mino2d'] = Combination(['embed2', 'CBC2d', 'CBC2dw', 'CBC2dr50w', 'cheat'],
                                       ['mino4_center*',
                                        'mino4_middle*'])
    
    combinations['old_nips_mino3d'] = Combination(['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'cheat'],
                                       ['mino4_grid24-*',
                                        'mino4_grid24art-*',
					])

    combinations['old_nips_fly'] = Combination(['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'cheat'],
                                       ['fly'])


    combinations['mino3d_tmp'] = Combination(['CBC3dw'],
                                       ['mino4_grid24-*',
                                        'mino4_grid24art-*',
                    ])

    combinations['mino3d_all'] = Combination(['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'cheat'],
                                       ['mino4_grid24-*',
                                        'mino4_patch32-*',
                                        'mino4_patch32s4-*',
                                        'mino4_midcen-*'])

    combinations['mino3dart'] = Combination(['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'cheat'],
                                       ['mino4_grid24art-*',
                                        'mino4_patch32art-*',
                                        'mino4_patch32s4art-*',
                                        'mino4_midcenart-*'])


    combinations['euclidean2d_tmp'] = Combination(['emds2', 'echeat', 'eCBC2dr50', 'eCBC2d',
                                                    'eCBC2dr80', 'eCBC2dr10'],
                                       ['E2-*'])

    nips_euclidean = ['emds2', 'echeat', 'eCBC2d']
    nips_spherical2d = ['embed2', 'cheat', 'CBC2d']
    nips_spherical2d_w = nips_spherical2d + [ 'CBC2dw']
    nips_spherical3d = ['embed3', 'cheat', 'CBC3d', 'CBC3dw']
    
  
    observable2d = ['rand-2D-fov315-pow3f-noisy',
                    'rand-2D-fov315-linear01-noisy',
                      'rand-2D-fov315-pow7f-noisy']
    
    unobservable2d = ['rand-2D-fov45-pow3_sat-noisy',
#                      'rand-2D-fov45-pow7_sat',
                      'rand-2D-fov45-linear01-noisy',
                      'rand-2D-fov90-pow3_sat-noisy',
#                      'rand-2D-fov90-pow7_sat',
                      'rand-2D-fov90-linear01-noisy']

    combinations['nips_euclidean'] = Combination(nips_euclidean,
                                       ['E2-grid-n180-eu_pow3',
                                        'E2-grid-n180-eu_pow7',
                                        'E2-grid-n180-eu_linear01'])
 
    combinations['nips_spherical_real_3d'] = Combination(nips_spherical3d,
                                       ['mino4_grid24-y_corr',
                                        'mino4_midcen-y_corr',
                                        'fly'])
#    combinations['nips_spherical_real_2d'] = Combination(nips_spherical2d,
#                                       )
#    
    combinations['nips_spherical_sim_2d_obs'] = Combination(nips_spherical2d_w,
                                                            observable2d)
    combinations['nips_spherical_sim_2d_unobs'] = Combination(nips_spherical2d,
                                                            unobservable2d + 
                                                            ['sick_front-y_corr',
                                                             'sick_front-y_dot_sign_corr',
                                                             'mino4_center-*'
                                                             ])
    
    combinations['GOPRO1'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w'],
        ['GOPRO-grid24-*',
        ' mino-grid24-*'])
  
    combinations['tmp2'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w',
          'CBC3dr50w_pi2', 'cheat'],
        ['GOPRO-grid24-*'])
  

    combinations['tmp3'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w',
          'CBC3dr50w_pi2', 'CBC3dw_15', 'cheat'],
        ['GOPRO-grid24-corr', 'GOPRO-grid24-art'])
  
  
    combinations['tmp4'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w',
          'CBC3dr50w_pi2', 'CBC3dw_15', 'cheat'],
        ['GOPRO-grid24-corr', 'mino-grid24-corr'])

    combinations['tmp5'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w',
          'CBC3dr50w_pi2', 'CBC3dw_15', 'cheat'],
        ['GOPRb-grid24-corr',
         'GOPRb-grid24-corr_n',
         'GOPRb-grid24-corr_m',
         'GOPRb-grid24-y_dot_corr',
         'GOPRb-grid24-y_dot_sign_corr',
         'GOPRb-grid24-art'])

    combinations['tmp6'] = Combination(
        [ 
         'cheat', 'CBC3dw', 'embed3' 
          ],
        [
         'GOPRb-grid20-corr' 
         ]) 
    
    
    combinations['tmp7'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w',
          'CBC3dr50w_pi2', 'CBC3dw_15', 'cheat'],
        ['GOPRb-grid24-corr',
         'GOPRb-grid24-corr_m',
         'GOPRb-grid24-art',
         'GOPRK-grid24-corr',
         'GOPRK-grid24-corr_m',
         'GOPRK-grid24-art',
         'mino-grid24-corr',
         'mino-grid24-corr_m',
         'mino-grid24-art',
         ])
    
    combinations['tmp8'] = Combination(
        ['embed3', 'CBC3dw', 'cheat'],
        ['omni-grid24-corr',
         'omni-grid24-corr_m',
         'omni-grid24-art'
         ])
    
    combinations['tmp9'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w',
          'CBC3dr50w_pi2', 'CBC3dw_15', 'cheat'],
        ['omni-grid16-corr',
         'omni-grid16-corr_m',
         'omni-grid16-corr_n',
         'omni-grid16-art'
         ])
    
    combinations['tmp10'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w',
          'CBC3dr50w_pi2', 'CBC3dw_15', 'cheat'],
        [
         'mino-grid24-corr_m',
         'omni-grid16-corr_m',
         'GOPRb-grid24-corr_m',
         'mino-grid24-art',
         'omni-grid16-art',
         'GOPRb-grid24-art'
         ])
    
    combinations['tmp11'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w',
          'CBC3dr50w_pi2', 'CBC3dw_15', 'cheat'],
        [
         'omni-grid16-*',
         'omni-grid8-*'
         ])
    
    combinations['tac-core'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w',
          'CBC3dr50w_pi2', 'CBC3dw_15', 'cheat'],
        [
         'mino-grid24-corr_m',
         'GOPRb-grid24-corr_m',
         'omni-grid8-corr_m',
         ])
    
    combinations['tac-core-art'] = Combination(
        ['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'CBC3dr10w',
          'CBC3dr50w_pi2', 'CBC3dw_15', 'cheat'],
        [
         'mino-grid24-art',
         'GOPRb-grid24-art',
         'omni-grid8-art'
         ])
    
    pami_algo_euclidean = ['emds2', 'echeat', 'eCBC2d']
    pami_algo_spherical2d = ['embed2', 'cheat', 'CBC2d']
    pami_algo_spherical2d_w = nips_spherical2d + [ 'CBC2dw']
    pami_algo_spherical3d = ['embed3', 'cheat', 'CBC3d', 'CBC3dw']
    
  
    pami_tc_observable2d = ['rand-2D-fov315-pow3f-noisy',
                    'rand-2D-fov315-linear01-noisy',
                      'rand-2D-fov315-pow7f-noisy']
    
    pami_tc_unobservable2d = ['rand-2D-fov45-pow3_sat-noisy',
#                      'rand-2D-fov45-pow7_sat',
                      'rand-2D-fov45-linear01-noisy',
                      'rand-2D-fov90-pow3_sat-noisy',
#                      'rand-2D-fov90-pow7_sat',
                      'rand-2D-fov90-linear01-noisy']

    combinations['pami_euclidean'] = Combination(pami_algo_euclidean,
                                       ['E2-grid-n180-eu_pow3',
                                        'E2-grid-n180-eu_pow7',
                                        'E2-grid-n180-eu_linear01'])
 
    combinations['pami_cameras'] = Combination(pami_algo_spherical3d,
                                       ['mino-grid24-corr_m',
                                         'GOPRb-grid24-corr_m',
                                         'omni-grid8-corr_m'])
                                    
    combinations['pami_cameras_art'] = Combination(pami_algo_spherical3d,
                                       ['mino-grid24-art',
                                        'GOPRb-grid24-art',
                                        'omni-grid8-art', ])
     
#    
    combinations['pami_spherical_sim_2d_obs'] = Combination(pami_algo_spherical2d_w,
                                                            pami_tc_observable2d)
    combinations['pami_spherical_sim_2d_unobs'] = Combination(pami_algo_spherical2d,
                                                            pami_tc_unobservable2d + 
                                                            [
                                                             'mino-center-corr_m',
                                                             'GOPRb-center-corr_m'
                                                             ])
    
    
    return combinations
