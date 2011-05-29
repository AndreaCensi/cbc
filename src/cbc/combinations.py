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
    
    combinations['mino3d'] = Combination(['embed3', 'CBC3d', 'CBC3dw', 'CBC3dr50w', 'cheat'],
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



    return combinations
