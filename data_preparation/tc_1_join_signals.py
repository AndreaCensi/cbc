#!/usr/bin/env python
from compmake import comp, compmake_console, use_filesystem
from tc_vars import Const
import numpy as np
import os
import tables
from tc_utils import desc


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

def log_load_from_hdf(filename):
    # These two just ignore the time
    f = tables.openFile(filename)
    y = np.array(f.root.procgraph.y[:]['value'])
    f.close()
    print('  hdf: loaded from %s: %s %s' % (filename, y.shape, y.dtype))
    return y

def log_write_to_hdf(filename, y):
    print('  hdf: writing to %s: %s %s' % (filename, y.shape, y.dtype))

    num = len(y)
    value = y[-1]
    print('Num: %s   last value: %s %s' % (num, value.dtype, value.shape))

    table_dtype = [ ('time', 'float64'),
                        ('value', value.dtype, value.shape) ]

    Z = np.zeros(shape=num, dtype=table_dtype)
    for i in range(num):
        Z['time'][i] = i
        Z['value'][i][:] = y[i]


    f = tables.openFile(filename, 'w')
    f.createGroup('/', 'procgraph')
    f.createTable('/procgraph', 'y', Z)
    f.close()

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
            y = log_load_from_hdf(filename)
            data.append(y)

        all_data = np.vstack(data)
        desc('first piece', data[0])
        desc('all_data', all_data)
        print('  all data: %s %s' % (all_data.shape, all_data.dtype))

        print('  creating %r' % master_signal)
        log_write_to_hdf(master_signal, all_data)


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
