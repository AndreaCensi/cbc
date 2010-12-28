import numpy as np

from reprep import Report 

from ..algorithms import CBCt, CBCt2 , CBC
from ..tools import get_cosine_matrix_from_s

def create_report_iterations(results):
    algo_class = results['algo_class'] 
    if algo_class in [ CBCt, CBCt2, CBC]:
        return plot_CBCt_iterations(results)
    else:
        return Report('cannot_draw')

def zero_diagonal(R):
    ''' Returns a copy with diagonal set to zero. '''
    n = R.shape[0]
    return R * (1 - np.eye(n))

def plot_CBCt_iterations(results, nid='CBCt_iterations'):
    R = results['R']
    true_C = results['true_C']
    iterations = results['iterations']
    R_order = iterations[0]['R_order']

    true_dist = np.real(np.arccos(true_C))

    r = Report(nid)
    f = r.figure(cols=3, caption='Data and ground truth')
    f.data('R', R).display('posneg', max_value=1).add_to(f, 'Given R')
    f.data('R0', zero_diagonal(R)).display('posneg', max_value=1).\
        add_to(f, 'Given R (diagonal set to 0).')
    
    f.data('R_order', R_order).display('scale').add_to(f, 'Order for R')
    
    with r.data_pylab('r_vs_c') as pylab:
        pylab.plot(true_C.flat, R.flat, '.', markersize=0.2)
        pylab.xlabel('real cosine')
        pylab.ylabel('correlation measure')
        pylab.axis((-1, 1, -1, 1))
    f.sub('r_vs_c', 'Unknown function cosine -> correlation')

    r.data('true_C', true_C).display('posneg', max_value=1).add_to(f, 'ground truth cosine matrix')
    r.data('gt_dist', true_dist).display('scale').add_to(f, 'ground truth distance matrix')

    
    has_more = results['algo_class'] in [ CBCt, CBCt2]
        
    cols = 6
    if has_more: cols += 2
    fit = r.figure(cols=cols)
    
    for i, it in enumerate(iterations): 
        rit = r.node('iteration%2d' % i)
        
        
        
        def display_posneg(what, caption="no desc"):
            data = it[what]
            nid = what
            n = rit.data(nid, data)
            n.display('posneg', max_value=1)
            fit.sub(n, caption=caption + ' (``%s``)' % what)

        def display_coords(nid, coords, caption=None):    
            n = rit.data(nid, coords)
            with n.data_pylab('plot') as pylab:
                plot_coords(pylab, coords)
            fit.sub(n, caption=caption)
        
        display_coords('current_guess_for_S', it['current_guess_for_S'],
                       'Current guess for coordinates.')
        display_posneg('guess_for_C', 'Cosines corresponding to guess for S.')
        display_posneg('new_estimated_C', 'Current guess for cosine matrix')
        
        if has_more:
            display_posneg('dont_trust', 'Areas we do not trust.')
            display_posneg('careful_C', 'The updated version of C.')
        
        
        display_coords('new_guess_for_S', it['new_guess_for_S'],
                       'New guess for coordinates (errors %.2f / %.2f deg)' % 
                       (it['error_deg'], it['rel_error_deg']))
        
        new_C = get_cosine_matrix_from_s(it['new_guess_for_S'])
        with rit.data_pylab('r_vs_est_c') as pylab:
            pylab.plot(new_C.flat, R.flat, '.', markersize=0.2)
            pylab.ylabel('estimated cosine')
            pylab.xlabel('correlation measure')
            pylab.axis((-1, 1, -1, 1))
        fit.sub('r_vs_est_c', 'R vs current C')
            
#        rit.data('Cest', it['Cest']).display('posneg', max_value=1).add_to(f, 'Cest')
#        rit.data('dont_trust', it['dont_trust'] * 1.0).display('scale').add_to(f, 'trust')
#        rit.data('Cestn', it['Cestn']).display('posneg', max_value=1).add_to(f, 'Cestn')
#        dist = np.real(np.arccos(it['Cestn']))
#        rit.data('dist', dist).display('scale', max_value=np.pi).add_to(f, 'corresponding distance')

#        distp = propagate(dist)
#        rit.data('distp', distp).display('scale', max_value=np.pi).add_to(f, 'propagated distance')
        
#        n = rit.data('singular_values', singular_values)
#        with n.data_pylab('plot') as pylab:
#            s = singular_values 
#            s = s / s[0]
#            pylab.plot(s[:15], 'x-')
#        f.sub(n, 'Singular values')
        
#
#        n = rit.data('coords_proj', coords)
#        with n.data_pylab('plot') as pylab:
#            pylab.plot(coords_proj[0, :], coords_proj[1, :], '.')
#            pylab.axis((-1, 1, -1, 1))
#        f.sub(n, 'Coordinates (projected)')
#        
#        with n.data_pylab('r_vs_est_c') as pylab:
#            pylab.plot(estimated_C.flat, R.flat, '.', markersize=0.2)
#            pylab.ylabel('estimated cosine')
#            pylab.xlabel('correlation measure')
#            pylab.axis((-1, 1, -1, 1))
#        f.sub('r_vs_est_c', 'R vs estimated C')
#            
#        with n.data_pylab('order_order') as pylab:
#            pylab.plot(estimated_C_order.flat, R_order.flat, '.', markersize=0.2)
#            pylab.ylabel('est C order')
#            pylab.xlabel('R order')
#        f.sub('order_order')
    return r

def plot_coords(pylab, coords):
    pylab.plot(coords[0, :], coords[1, :], 'k-')
    pylab.plot(coords[0, :], coords[1, :], '.')
    pylab.axis('equal')

