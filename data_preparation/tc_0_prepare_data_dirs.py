from contracts import contract
from file_utils import should_exist
from procgraph import pg
from tc_utils import filter_S
from tc_vars import Const
import cPickle as pickle
import os
import scipy.io

        
def main():
  
    for video in Const.videos:
        mp4 = os.path.join(Const.data_dir, '%s.mp4' % video)

        should_exist(mp4)

        calibration = os.path.join(Const.data_dir, '%s_calibration.mat' % video)
        if os.path.exists(calibration):
            S = get_groundtruth(calibration)
        else:
            print('  No ground truth file %r found.' % calibration)
            S = None

        for conf_id, config in Const.filters.items():
            print('* Creating %s - %s ' % (video, conf_id))
            
            filter = config['filter'] #@ReservedAssignment
            #ndim = config['ndim']
            
            signal_name = '%s-%s' % (video, conf_id)
            signal_dir = os.path.join(Const.signals_dir, signal_name)
            if not os.path.exists(signal_dir):
                os.makedirs(signal_dir)
            
            # copy signal
            signal_file = os.path.join(signal_dir, Const.SIGNAL_FILE) 
            ground_truth_file = os.path.join(signal_dir, Const.GT_FILE)
    
            extract_data(mp4, filter_name=conf_id, hdf=signal_file)
            should_exist(signal_file)
        
            if S is not None:
                true_S = filter_S(S, config['filter'], 3) 
                
#                if not os.path.exists(ground_truth_file):
                print('  Writing out gt file %r (shape %s).' % 
                      (ground_truth_file, true_S.shape))
                with open(ground_truth_file, 'wb') as f:
                    pickle.dump({'true_S': true_S}, f)
            else:
                print('  No ground truth found.')


    
def extract_data(video, filter_name, hdf):
    if os.path.exists(hdf): 
        #print('  File %r already exists.' % hdf)
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
#    elif 'X' in data:
#        print 'X shape: %s' % str(data['X'].shape)
#        print 'Y shape: %s' % str(data['Y'].shape)
#        X = data['X'].T
#        Y = data['Y'].T
#        Z = data['Z'].T
#        h, w = X.shape
#        S = np.zeros((h, w, 3))
#        S[:, :, 0] = X
#        S[:, :, 1] = Y
#        S[:, :, 2] = Z
#        
#         
#        return S
    raise Exception('Unknown format (%r).' % data.keys())

        
    
    
if __name__ == '__main__':
    main()
    
    
    
