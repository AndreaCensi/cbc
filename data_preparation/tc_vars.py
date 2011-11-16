from tc_filters import grid24, midcen, patch32s4, patch32, middle, center
from tc_stats import y_dot_sign_corr, y_dot_corr, y_corr, artificial

class Const:
    data_dir = 'data/'
    videos = [
#      'mino02', 'mino03', 'mino05', 'mino06',
        'GOPR0612',
        'GOPR0613', 'GOPR0614', 'GOPR0615'
    ]
    
    signals_dir = 'signals/'
    tc_dir = 'test_cases/'
    SIGNAL_FILE = 'signal.h5'
    GT_FILE = 'ground_truth.pickle'
    TC_FILE = 'stats.pickle'
    
    filters = {
        'center':    dict(filter=center, ndim=2),
        'middle':    dict(filter=middle, ndim=2),
        'patch32':   dict(filter=patch32, ndim=3),
        'patch32s4': dict(filter=patch32s4, ndim=3),
        'midcen':    dict(filter=midcen, ndim=3),
        'grid24':    dict(filter=grid24, ndim=3),
    }
    
    osets = { 
        'GOPRO': ['GOPR0612',
                  'GOPR0613', 'GOPR0614', 'GOPR0615'
                  ],
        #'mino': ['mino02', 'mino03', 'mino05', 'mino06']
    }
             
    stats = {  
        'corr': dict(id='corr', function=y_corr, needs_gt=False, desc=""),
        'y_dot_corr': dict(id='y_dot_corr', function=y_dot_corr, needs_gt=False, desc=""),
        'y_dot_sign_corr': dict(id='y_dot_sign_corr', function=y_dot_sign_corr, needs_gt=False, desc=""),
        'art': dict(id='art', function=artificial, needs_gt=True, desc=""),
    }

