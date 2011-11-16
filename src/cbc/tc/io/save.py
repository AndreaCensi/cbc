import os, cPickle as pickle
from contracts import contract
import yaml

@contract(R='array[NxN]', true_S='None|array[3xN]')
def tc_write(dirname, tc_id, R, true_S, attrs={}):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    tc_file = '%s.data.pickle' % tc_id
    gt_file = '%s.gt.pickle' % tc_id
    yaml_file = '%s.tc.yaml' % tc_id

    #print(' Writing to %r' % tc_file)
    with open(os.path.join(dirname, tc_file), 'wb') as f:
        pickle.dump(dict(similarity=R), f)
        
    if true_S is not None:
        # TODO: check
        #print(' Writing to %r' % gt_file)
        with open(os.path.join(dirname, gt_file), 'wb') as f:
            pickle.dump(dict(true_S=true_S), f)
    else: 
        gt_file = None
        
    with open(os.path.join(dirname, yaml_file), 'w') as f:
        yaml.dump([{
         'id': tc_id,
         'attrs': attrs,
         'file:data':tc_file,
         'file:gt': gt_file,
         'format': ['calib_pickle', [1, 0]],
         'format_desc': ((
'The file ``%s`` contains a dictionary with a field ``similarity``,'
'which is a numpy array of size %s (%s).\n'

'The file ``%s`` contains a dictionary with a field ``true_S``, '
'which is a numpy array of size %s (%s).'     
         ) % (tc_file, R.shape, R.dtype,
                gt_file, R.dtype, true_S.dtype)).strip()
        }], f, default_flow_style=False)

        
