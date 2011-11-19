from compmake import comp, compmake_console, use_filesystem
from tc_vars import Const
import numpy as np
import os
import tables

def main():
    use_filesystem(os.path.join(Const.signals_dir, 'compmake_join'))
     
    sets = {}
    for fname in Const.filters.keys():
        mkname = lambda x: '%s-%s' % (x, fname)
        for master, pieces in Const.osets.items():
            sets[mkname(master)] = [mkname(x) for x in pieces]
        
    for master, pieces in sets.items():
        comp(join_signals, master, pieces,
             job_id='join-%s' % master)
        
    compmake_console()
    
def join_signals(master, pieces):
    print('* Creating %r from %s' % (master, pieces))
    master_dir = os.path.join(Const.signals_dir, master)
    if not os.path.exists(master_dir):
        os.makedirs(master_dir)
    master_signal = os.path.join(master_dir, Const.SIGNAL_FILE)

    if not os.path.exists(master_signal):
    
        data = []
        for piece in pieces:
            filename = os.path.join(Const.signals_dir, piece,
                                    Const.SIGNAL_FILE)
            f = tables.openFile(filename)
            y = np.array(f.root.procgraph.y[:])
            print('  - loaded piece %s: %s %s' % (piece, y.shape, y.dtype))

            data.append(y)
            f.close()
    
        all_data = np.hstack(data)
        print('  all data: %s %s' % (all_data.shape, all_data.dtype))
    
        print('  creating %r' % master_signal)
        f = tables.openFile(master_signal, 'w')
        f.createGroup('/', 'procgraph')
        f.createTable('/procgraph', 'y', all_data)
        f.close()

    gt = os.path.join(Const.signals_dir, pieces[0], Const.GT_FILE)
    gtm = os.path.join(Const.signals_dir, master, Const.GT_FILE)
    if os.path.exists(gt):
        if os.path.exists(gtm):
            os.unlink(gtm)
        print('  copying ground truth %r' % gtm)
        os.link(gt, gtm)
    else:
        msg = ('  (no ground truth %r found)' % gt)
        raise Exception(msg)
        
        


if __name__ == '__main__':
    main()
