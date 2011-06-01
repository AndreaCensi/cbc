''' Collection of plotting utils. '''
from contracts import contract
import numpy as np
from ..tools import create_histogram_2d

@contract(S='array[2xN]')
def util_plot_euclidean_coords2d(report, f, nid, S):
    with report.data_pylab(nid) as pylab: 
        pylab.plot(S[0, :], S[1, :], '.')
        pylab.axis('equal')
        pylab.xlabel('x1')
        pylab.ylabel('x2')
    report.last().add_to(f)
    
def add_order_comparison_figure(report, nid, figure, caption,
                                x_order, y_order, xlabel, ylabel):
    x_order = np.array(x_order.flat)
    y_order = np.array(y_order.flat)
    n = x_order.size
    assert x_order.max() == n - 1
    assert y_order.max() == n - 1
    with report.data_pylab(nid, figsize=(6, 6)) as pylab:
        pylab.plot(x_order, y_order, 'k.', markersize=0.2)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        pylab.xticks([], [])
        pylab.yticks([], [])
        pylab.axis([0, n - 1, 0, n - 1])
#        pylab.axis('equal')
#        pylab.axis([0, n - 1, 0, n - 1])
    report.last().add_to(figure, caption)

def plot_and_display_coords(r, f, nid, coords, caption=None):    
    n = r.data(nid, coords)
    with n.data_pylab('plot') as pylab:
        pylab.plot(coords[0, :], coords[1, :], 'k-')
        pylab.plot(coords[0, :], coords[1, :], '.')
        pylab.axis('equal')
        pylab.xlabel('x1')
        pylab.ylabel('x2')
    f.sub(n, caption=caption)


def util_plot_xy_generic(r, f, nid, x, y, xlabel, ylabel, caption):
    with r.data_pylab(nid) as pylab:
        pylab.plot(x, y, 'b.', markersize=0.2)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
#            pylab.axis((-1, 1, -1, 1))
    r.last().add_to(f, caption)
        

def plot_one_against_the_other(r, nid, xval, yval):
    h = create_histogram_2d(xval, yval, resolution=128)
    n = r.data(nid, np.flipud(h.T)).display('scale')
    return n 

def zero_diagonal(R):
    ''' Returns a copy with diagonal set to zero. '''
    n = R.shape[0]
    return R * (1 - np.eye(n))


