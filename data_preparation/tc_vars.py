from tc_filters import grid24, midcen, middle, center, grid16, grid20, grid8
from tc_stats import (y_dot_sign_corr, y_dot_corr, y_corr, artificial,
    y_corr_norm, y_corr_m)


class Const:
    data_dir = 'calib_data/'
    signals_dir = 'signals/'
    tc_dir = 'test_cases/'

    SIGNAL_FILE = 'signal.h5'
    GT_FILE = 'ground_truth.pickle'
    TC_FILE = 'stats.pickle'

    MASK_PATTERN = '%s_mask.png'
    CALIBRATION_PATTERN = '%s_calibration.mat'

    videos = [
        'mino02', 'mino03', 'mino05', 'mino06',
        'mino87', 'mino88', 'mino89',

        'GOPR0612',
        'GOPR0613',
        'GOPR0614',
        'GOPR0615',

        'GOPRb0674',
        'GOPRb0675',
        'GOPRb0676',
        'GOPRb0701',
        'GOPRb0702',
        'GOPRb0703',
        'GOPRb0704',
        'GOPRb0705',

    ]

    omni_videos = ['omni02', 'omni03']

    videos.extend(omni_videos)

#    videos_rgb = []
#    for k in ['r', 'g', 'b']:
#        for x in [        
#        'GOPRb0674',
#        'GOPRb0675',
#        'GOPRb0676',
#        'GOPRb0701',
#        'GOPRb0702',
#        'GOPRb0703',
#        'GOPRb0704',
#        ]:
#            videos_rgb.append('%s%s' % (x, k))
#    videos.extend(videos_rgb)

    filters = {
        'center': dict(filter=center, ndim=2),
        'middle': dict(filter=middle, ndim=2),
#        'patch32':   dict(filter=patch32, ndim=3),
#        'patch32s4': dict(filter=patch32s4, ndim=3),
        'midcen': dict(filter=midcen, ndim=3),
        'grid24': dict(filter=grid24, ndim=3),
        'grid20': dict(filter=grid20, ndim=3),
        'grid16': dict(filter=grid16, ndim=3, only=omni_videos + ['omni']),
        'grid8': dict(filter=grid8, ndim=3, only=omni_videos + ['omni'])
    }

    osets = {
        'GOPRO': ['GOPR0612', 'GOPR0613', 'GOPR0614', 'GOPR0615'],
        'GOPRb': ['GOPRb0674',
                  'GOPRb0675',
                  'GOPRb0676',
                  'GOPRb0701',
                  'GOPRb0702',
                  'GOPRb0703',
                  'GOPRb0704',
                  'GOPRb0705'],
#        'GOPRK': videos_rgb,
        'mino': ['mino02', 'mino03', 'mino05', 'mino06',
                 'mino87', 'mino88', 'mino89'],
        'omni': omni_videos
    }

    stats = {
        'corr': dict(id='corr', function=y_corr, needs_gt=False, desc=""),
        'corr_m': dict(id='corr_m', function=y_corr_m, needs_gt=False,
                       desc=""),
        'y_dot_corr': dict(id='y_dot_corr', function=y_dot_corr,
                           needs_gt=False, desc=""),
        'y_dot_sign_corr': dict(id='y_dot_sign_corr', function=y_dot_sign_corr,
                                needs_gt=False, desc=""),
        'art': dict(id='art', function=artificial, needs_gt=True, desc=""),
        'corr_n': dict(id='corr', function=y_corr_norm, needs_gt=False,
                       desc=""),
    }

