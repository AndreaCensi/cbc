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
    
def add_order_comparison_figure(report, figure, caption, x_order, y_order, xlabel, ylabel):
    with report.data_pylab(caption) as pylab:
        pylab.plot(x_order.flat, y_order.flat, '.', markersize=0.2)
        pylab.axis('equal')
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
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
    

#def plot_coords(pylab, coords):
#        pylab.plot(coords[0, :], coords[1, :], 'k-')
#        pylab.plot(coords[0, :], coords[1, :], '.')
#        pylab.axis('equal')

def plot_one_against_the_other(r, nid, xval, yval):
    h = create_histogram_2d(xval, yval, resolution=128)
    n = r.data(nid, np.flipud(h.T)).display('scale')
    return n 

def zero_diagonal(R):
    ''' Returns a copy with diagonal set to zero. '''
    n = R.shape[0]
    return R * (1 - np.eye(n))


