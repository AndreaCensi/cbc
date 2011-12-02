''' Collection of plotting utils. '''
from . import contract, np
from ..tools import create_histogram_2d


fsize = 2.5

@contract(S='array[2xN]')
def util_plot_euclidean_coords2d(report, f, nid, S):
    with report.plot(nid, figsize=(3, 3)) as pylab: 
        pylab.plot(S[0, :], S[1, :], '.')
        pylab.axis('equal')
#        pylab.xlabel('x1')
#        pylab.ylabel('x2')

    report.last().add_to(f)
    
    

def add_distance_vs_sim_figure(report, nid, figure, caption,
                                D, R, xlabel, ylabel):
    D = np.array(D.flat)
    R = np.array(R.flat)
    
    with report.plot(nid, figsize=(fsize, fsize)) as pylab:
        pylab.plot(D, R, 'k.', markersize=0.2)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        pylab.yticks([], [])
        pylab.axis([D.min(), D.max(), R.min(), R.max()])
#        xt, xl = pylab.xticks()
#        pylab.xticks([xt[0], xt[-1]], [xl[0].get_text(), xl[-1].get_text()])
        m = D.max()
        pylab.xticks([0, m], ['0', '%.2f' % m])

    report.last().add_to(figure, caption)
    

def add_order_comparison_figure(report, nid, figure, caption,
                                x_order, y_order, xlabel, ylabel):
    x_order = np.array(x_order.flat)
    y_order = np.array(y_order.flat)
    n = x_order.size
    assert x_order.max() == n - 1
    assert y_order.max() == n - 1
    with report.plot(nid, figsize=(fsize, fsize)) as pylab:
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
    with n.plot('plot', figsize=(fsize, fsize)) as pylab:
#        pylab.plot(coords[0, :], coords[1, :], 'k-')
        pylab.plot(coords[0, :], coords[1, :], '.')
#        pylab.axis([coords[0, :].min(), coords[0, :].max(),
#                    coords[1, :].min(), coords[1, :].max()])
        pylab.axis('equal')
        pylab.xlabel('x1')
        pylab.ylabel('x2')
    f.sub(n, caption=caption)


def util_plot_xy_generic(r, f, nid, x, y, xlabel, ylabel, caption):
    with r.plot(nid) as pylab:
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


