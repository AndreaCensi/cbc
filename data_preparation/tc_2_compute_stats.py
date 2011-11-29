#!/usr/bin/env python
from cbc.tc.io.save import tc_write
from compmake import comp, compmake_console, use_filesystem
from tc_utils import reshape
from tc_vars import Const
import cPickle as pickle
import itertools
import numpy as np
import os
import tables

def list_signals():
    candidates = os.listdir(Const.signals_dir)
    final = [ x for x in candidates if not x[0] == '.']
    return final

def signal_read_data(signal):
    filename = os.path.join(Const.signals_dir, signal, Const.SIGNAL_FILE)
    f = tables.openFile(filename)
    Y = f.root.procgraph.y[:]['value']
    Y = np.array(Y).astype('float32')
    f.close()
    return Y
        
def signal_read_ground_truth(signal):
    gt_file = os.path.join(Const.signals_dir, signal, Const.GT_FILE)
    if not os.path.exists(gt_file):
        return None
    with open(gt_file, 'rb') as f:
        data = pickle.load(f)
    return data['true_S']
    
    
def main():
    use_filesystem(os.path.join(Const.signals_dir, 'compmake_stats'))
    
#    signals = list_signals() # only do the compound ones
#    signals = Const.osets.keys()
    for id_oset, id_filter, id_stat in itertools.product(Const.osets, Const.filters, Const.stats):
        signal = '%s-%s' % (id_oset, id_filter)
        comp(compute_and_write_stats, signal, id_stat,
             job_id='stats-%s-%s' % (signal, id_stat))

    compmake_console()
            
def compute_and_write_stats(signal, stat):
    tc_id = '%s-%s' % (signal, stat)

    # Read data
    true_S = signal_read_ground_truth(signal)
    if true_S is None:
        print('No ground truth available.')
      
    y = signal_read_data(signal)

    if true_S is not None:
        print('* signal %r: y.shape: %r  true_S.shape: %r' % 
              (signal, y.shape, true_S.shape))

        y, true_S = reshape(y, true_S)
    
        print('* signal %r: %r %r' % (signal, y.shape, true_S.shape))

    if true_S is None and Const.stats[stat]['needs_gt']: 
        print('Not computing %s because ground truth not available.' % tc_id)
        return
    
    stat_function = Const.stats[stat]['function']
    #stat_desc = Const.stats[stat]['desc']

    # Compute stats
    R = stat_function(y, true_S)
    if R is None:
        raise Exception('* Could not compute tc %r' % tc_id)
        

    # Write it out
    statistic = dict(**Const.stats[stat])
    statistic['code'] = statistic['function'].__name__
    statistic.pop('function')
    
    dirname = os.path.join(Const.tc_dir, tc_id)    
    tc_write(dirname=dirname,
             tc_id=tc_id,
             R=R,
             true_S=true_S,
             attrs={'signal': signal,
                    'statistic': statistic,
                    'signal_shape': list(y.shape)})
    
if __name__ == '__main__':
    main()
