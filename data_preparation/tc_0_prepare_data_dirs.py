#!/usr/bin/env python
from contracts import contract
from file_utils import should_exist
from procgraph import pg
from tc_utils import filter_S, desc, filter_S_keep_dim
from tc_vars import Const
import cPickle as pickle
import itertools
import numpy as np
import os
import scipy.io
import Image
from tc_1_join_signals import log_load_from_hdf, log_write_to_hdf

        
def main():
    from compmake import comp, compmake_console, use_filesystem
    use_filesystem(os.path.join(Const.signals_dir, 'compmake'))
    for id_video, id_filter in itertools.product(Const.videos, Const.filters):
        comp(extract_signals, id_video, id_filter,
             job_id='extract-%s-%s' % (id_video, id_filter))
    compmake_console()

def find_stem(s): 
    ''' Removes numbers from a string '''
    for i in range(10):
        s = s.replace('%d' % i, '')
    return s

def extract_signals(id_video, id_filter):
    filter_function = Const.filters[id_filter]['filter']
    
    mp4 = os.path.join(Const.data_dir, '%s.mp4' % id_video)
    should_exist(mp4)
    
    stem = find_stem(id_video)
    
    # TODO: use stem
    calibration = os.path.join(Const.data_dir, Const.CALIBRATION_PATTERN % stem)
    if os.path.exists(calibration):
        S = get_groundtruth(calibration)
    else:
        print('No ground truth file %r found.' % calibration)
        S = None

    maskfile = os.path.join(Const.data_dir, Const.MASK_PATTERN % stem)
    if os.path.exists(maskfile):
        mask = get_mask(maskfile)
        mask_select = filter_function(mask)
    else:
        print('No mask file %r found.' % maskfile)
        mask = None

    print('Creating %s - %s ' % (id_video, id_filter))

    signal_name = '%s-%s' % (id_video, id_filter)
    signal_dir = os.path.join(Const.signals_dir, signal_name)
    if not os.path.exists(signal_dir):
        os.makedirs(signal_dir)
    
    # copy signal
    signal_file = os.path.join(signal_dir, Const.SIGNAL_FILE) 

    if mask is None:
        # No mask, creting normal file
        extract_data(mp4, filter_name=id_filter, hdf=signal_file)
    else:
        # Write to temp file
        tmp_file = signal_file + '.without_mask'
        extract_data(mp4, filter_name=id_filter, hdf=tmp_file)
        y = log_load_from_hdf(tmp_file)
        desc('y', y)
        y0 = y[0]
        desc('y0', y0)
        desc('mask_select', mask_select)
        
        y0_sel = y0[mask_select]
        desc('y0_sel', y0_sel)
        print('Number selected: %s' % np.sum(mask_select))
        y_sel = y[..., mask_select]
        desc('y_sel', y_sel)
        
        log_write_to_hdf(signal_file, y_sel)
    
    should_exist(signal_file)

    if S is not None:
        if mask is  None:
            desc('S', S)
            true_S = filter_S(S, filter_function, 3)
            desc('true_S', true_S)
        else:
            true_S = filter_S_keep_dim(S, filter_function)
            desc('true_S', true_S)
            true_S = true_S[:, mask_select]
            desc('true_S (after mask)', true_S)
            
        write_arrays_to_pickle(
                 os.path.join(signal_dir, Const.GT_FILE),
                 {'true_S': true_S}              
        )
    else:
        print('No ground truth found.')
     

def write_arrays_to_pickle(filename, data):
    print('Writing on file %r.' % filename)
    for k, v in data.items():
        if isinstance(v, np.ndarray):
            print('- %20s: %10s %s' % (k, v.dtype, v.shape))  
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    

def extract_data(video, filter_name, hdf):
    if os.path.exists(hdf): 
        return

    print('  Creating %r...' % hdf)
    pg('extract_some',
        config={'file': video, 'filter': filter_name, 'hdf': hdf})

    
@contract(returns='array[HxWx3]')
def get_groundtruth(calibration):
    # Load groundtruth
    data = scipy.io.loadmat(calibration)
    if 'S' in data:
        S = data['S']  
        return S
    elif 'X' in data:
        # print 'X shape: %s' % str(data['X'].shape)
        # print 'Y shape: %s' % str(data['Y'].shape)
        X = data['X']
        Y = data['Y']
        Z = data['Z']
        h, w = X.shape
        S = np.zeros((h, w, 3))
        S[:, :, 0] = X
        S[:, :, 1] = Y
        S[:, :, 2] = Z
        # print('S shape: %r' % str(S.shape))
        return S
    raise Exception('Unknown format (%r).' % data.keys())


def get_mask(filename):
    ''' Loads the mask from a .png file. '''
    data = np.array(Image.open(filename))
    print('Loaded mask size  %s %s' % (data.dtype, str(data.shape)))
    data = data[:, :, 1] 
    threshold = np.mean(data)
    print('data mean: %s' % threshold)
    data = data > threshold
    print(' selected: %d / %d = %.1f%%' % 
          (np.sum(data), data.size, np.sum(data) * 100.0 / data.size))
    return data
        
    
if __name__ == '__main__':
    main()
    
    
    
