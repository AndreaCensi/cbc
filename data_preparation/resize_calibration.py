import scipy.io
import numpy as np
import scipy.ndimage
from numpy.testing.utils import assert_allclose
from reprep import Report

def get_S(data):
    X = data['X']
    Y = data['Y']
    Z = data['Z']
    h, w = X.shape
    S = np.zeros((h, w, 3))
    S[:, :, 0] = X
    S[:, :, 1] = Y
    S[:, :, 2] = Z
    return S

def resize(m, target_size):
    print('orig shape: %s' % str(m.shape))
    print('    target: %s' % str(target_size))
    
    ratios = []
    for i in range(2):
        ratios.append(1.0 * target_size[i] / m.shape[i])
        
    print('zoom: %s' % ratios)
#    print('original*zoom: %s' % str((m.shape[0] * zoom, m.shape[1] * zoom)))
    m2 = scipy.ndimage.interpolation.zoom(m, ratios, mode='nearest', order=2)
    
    print('obtained: %s' % str(m2.shape))

    assert_allclose(m2.shape, target_size)
    return m2


    
file1 = 'data/GOPR_groundtruth_orig.mat' 
file2 = 'data/GOPR_groundtruth.mat'

orig_size = (1944, 2592)
target_size = (1080, 1920) 

        
data1 = scipy.io.loadmat(file1)
data2 = {}
for k in ['X', 'Y', 'Z']:
    data2[k] = resize(data1[k], target_size).astype('float32')

data2['S'] = get_S(data2)

#data2['before_resizing'] = data1
scipy.io.savemat(file2, data2, oned_as='row')
        
r = Report()

def go(name, data):
    f = r.figure(name)
    for a in ['X', 'Y', 'Z']:
        print name, a, data[a].shape
        f.data(a, data[a]).display('posneg').add_to(f)

go('data1', data1)
go('data2', data2)
r.to_html('data/resizing/index.html')

