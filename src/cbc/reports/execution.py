import numpy as np

from reprep import Report 

from ..algorithms import CBCt, CBCt2 , CBC
from ..tools import get_cosine_matrix_from_s
from snp_geometry.utils import assert_allclose
from cbc.tools.math_utils import create_s_from_theta, get_angles_from_S, \
    scale_score, find_closest_multiple

def create_report_iterations(exc_id, results):
    r = Report(exc_id)
    algo_class = results['algo_class'] 
    if algo_class in [ CBCt, CBCt2, CBC]:
        r.add_child(create_report_CBCt_iterations(results))

    r.add_child(create_report_final_solution(results))
    return r

def zero_diagonal(R):
    ''' Returns a copy with diagonal set to zero. '''
    n = R.shape[0]
    return R * (1 - np.eye(n))

def create_report_final_solution(results):
    r = Report('final_solution')
    
    true_S = results['true_S']
    S_aligned = results['S_aligned']
    
    f = r.figure('Comparisons with ground truth', cols=4)
    solutions_comparison_plots(r, f, true_S, S_aligned)
    return r
        
        
def plot_and_display_coords(r, f, nid, coords, caption=None):    
    n = r.data(nid, coords)
    with n.data_pylab('plot') as pylab:
        plot_coords(pylab, coords)
    f.sub(n, caption=caption)

def solutions_comparison_plots(r, f, true_S, S_aligned):
    true_theta = np.degrees(get_angles_from_S(true_S))
    theta = np.degrees(get_angles_from_S(S_aligned))
    
    theta = find_closest_multiple(theta, true_theta, 360)

    plot_and_display_coords(r, f, 'true_S', true_S, 'Ground truth')
    plot_and_display_coords(r, f, 'S_aligned', S_aligned, 'Solution, aligned')

    with r.data_pylab('sol_compare') as pylab:
        for i in range(len(theta)):
            pylab.plot([0, 1], [true_theta[i], theta[i]], '-')
    f.sub('sol_compare', 'Estimated (left) and true (right) angles.')
     
    with f.data_pylab('theta_compare') as pylab:
        pylab.plot(true_theta, theta, '.')
        pylab.xlabel('true angles (deg)')
        pylab.ylabel('estimated angles (deg)')
        pylab.axis('equal')
    f.sub('theta_compare', 'True vs estimated angles.')
         
        
def create_report_CBCt_iterations(results):
    r = Report('CBC_iterations')

    R = results['R']
    true_C = results['true_C']
    iterations = results['iterations']
    R_order = iterations[0]['R_order']

    true_dist = np.real(np.arccos(true_C))

    f = r.figure(cols=3, caption='Data and ground truth')
    f.data('R', R).display('posneg', max_value=1).add_to(f, 'Given R')
    f.data('R0', zero_diagonal(R)).display('posneg', max_value=1).\
        add_to(f, 'Given R (diagonal set to 0).')
    
    r.data('R_order', R_order).display('scale').add_to(f, 'Order for R')
    
    with r.data_pylab('r_vs_c') as pylab:
        pylab.plot(true_C.flat, R.flat, '.', markersize=0.2)
        pylab.xlabel('real cosine')
        pylab.ylabel('correlation measure')
        pylab.axis((-1, 1, -1, 1))
    r.last().add_to(f, 'Unknown function cosine -> correlation')

    r.data('true_C', true_C).display('posneg', max_value=1).add_to(f, 'ground truth cosine matrix')
    r.data('gt_dist', true_dist).display('scale').add_to(f, 'ground truth distance matrix')

    
    has_more = results['algo_class'] in [ CBCt, CBCt2]
        
    cols = 7
    if has_more: cols += 2
    fit = r.figure(cols=cols)
    
    for i, it in enumerate(iterations): 
        rit = r.node('iteration%d' % i)
        
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
            pylab.xlabel('estimated cosine')
            pylab.ylabel('correlation measure')
            pylab.axis((-1, 1, -1, 1))
        rit.last().add_to(fit, 'R vs current C') 
        
        new_C_order = scale_score(new_C)
        with rit.data_pylab('r_order_vs_est_c_order') as pylab:
            pylab.plot(new_C_order.flat, R_order.flat, '.', markersize=0.2)
            pylab.xlabel('estimated cosine (order)')
            pylab.ylabel('correlation measure (order)')
        rit.last().add_to(fit, 'order comparison (spearman: %f)' % 
                            it['spearman'])

        if False: # too fancy 
            with rit.data_pylab('sol_compare') as pylab:
                true_theta = get_angles_from_S(results['true_S'])
                theta = get_angles_from_S(it['S_aligned'])
                for i in range(len(theta)):
                    pylab.plot([0, 1], [true_theta[i], theta[i]], '-')
            fit.sub(rit.resolve_url('sol_compare'), 'Estimated (left) and true (right) angles.')
        
        # if groundtruth
        with rit.data_pylab('theta_compare') as pylab:
            true_theta = np.degrees(get_angles_from_S(results['true_S']))
            theta = np.degrees(get_angles_from_S(it['S_aligned']))
            pylab.plot(true_theta, theta, '.')
            pylab.xlabel('true angles (deg)')
            pylab.ylabel('estimated angles (deg)')
            pylab.axis('equal')
        fit.sub(rit.resolve_url('theta_compare'), 'True vs estimated angles.')
     
#        distp = propagate(dist)
#        rit.data('distp', distp).display('scale', max_value=np.pi).add_to(f, 'propagated distance')
        
#        n = rit.data('singular_values', singular_values)
#        with n.data_pylab('plot') as pylab:
#            s = singular_values 
#            s = s / s[0]
#            pylab.plot(s[:15], 'x-')
#        f.sub(n, 'Singular values')
        
    return r

def plot_coords(pylab, coords):
    pylab.plot(coords[0, :], coords[1, :], 'k-')
    pylab.plot(coords[0, :], coords[1, :], '.')
    pylab.axis('equal')

