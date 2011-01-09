import numpy as np

from reprep import Report 

#from ..algorithms import CBC
from ..tools import (scale_score, find_closest_multiple,
                     distances_from_cosines,
                     cosines_from_directions, angles_from_directions)

def create_report_iterations(exc_id, results):
    r = Report(exc_id)
    r.add_child(create_report_final_solution(results))

#    algo_class = results['algo_class'] 
#    if algo_class in [ CBCt, CBCt2, CBC]: #, CBCa]:
#        r.add_child(create_report_CBCt_iterations(results))
#    else:
    r.add_child(create_report_generic_iterations(results))

    return r

def zero_diagonal(R):
    ''' Returns a copy with diagonal set to zero. '''
    n = R.shape[0]
    return R * (1 - np.eye(n))

def create_report_final_solution(results):
    r = Report('final_solution')
    
    R = results['R']
    true_S = results['true_S']
    S_aligned = results['S_aligned']
    
    f = r.figure('unobservable_measures',
                 caption='Comparisons with ground truth (unobservable)', cols=4)
    
    if S_aligned.shape[0] == 2:
        solutions_comparison_plots(r, f, true_S, S_aligned)
    
    f2 = r.figure('observable_measures', cols=3, caption='Computable measures')
    C_order = scale_score(cosines_from_directions(S_aligned))
    R_order = scale_score(R)
    with r.data_pylab('r_order_vs_est_c_order') as pylab:
        pylab.plot(C_order.flat, R_order.flat, '.', markersize=0.2)
        pylab.xlabel('estimated cosine (order)')
        pylab.ylabel('correlation measure (order)')

    r.last().add_to(f2, 'order comparison (spearman: %.7f)' % results['spearman'])
        
    return r
        
def plot_and_display_coords(r, f, nid, coords, caption=None):    
    n = r.data(nid, coords)
    with n.data_pylab('plot') as pylab:
        plot_coords(pylab, coords)
    f.sub(n, caption=caption)

def solutions_comparison_plots(r, f, true_S, S_aligned):
    true_theta = np.degrees(angles_from_directions(true_S))
    theta = np.degrees(angles_from_directions(S_aligned))
    theta = find_closest_multiple(theta, true_theta, 360)

    plot_and_display_coords(r, f, 'true_S', true_S, 'Ground truth')
    plot_and_display_coords(r, f, 'S_aligned', S_aligned, 'Solution, aligned')

    with r.data_pylab('sol_compare') as pylab:
        for i in range(len(theta)):
            pylab.plot([0, 1], [true_theta[i], theta[i]], '-')
    f.sub('sol_compare', 'Estimated (left) and true (right) angles.')
     
    with r.data_pylab('theta_compare') as pylab:
        pylab.plot(true_theta, theta, '.')
        pylab.xlabel('true angles (deg)')
        pylab.ylabel('estimated angles (deg)')
        pylab.axis('equal')
    f.sub('theta_compare', 'True vs estimated angles.')
         
        
#def create_report_CBCt_iterations(results):
#    r = Report('CBC_iterations')
#
#    R = results['R']
#    true_C = results['true_C']
#    true_S = results['true_S']
#    iterations = results['iterations']
#    R_order = iterations[0]['R_order']
#
#    true_dist = np.real(np.arccos(true_C))
#
#    f = r.figure(cols=3, caption='Data and ground truth')
#    f.data('R', R).display('posneg', max_value=1).add_to(f, 'Given R')
#    f.data('R0', zero_diagonal(R)).display('posneg', max_value=1).\
#        add_to(f, 'Given R (diagonal set to 0).')
#    
#    r.data('R_order', R_order).display('scale').add_to(f, 'Order for R')
#    
#    with r.data_pylab('r_vs_c') as pylab:
#        pylab.plot(true_C.flat, R.flat, '.', markersize=0.2)
#        pylab.xlabel('real cosine')
#        pylab.ylabel('correlation measure')
#        pylab.axis((-1, 1, -1, 1))
#    r.last().add_to(f, 'Unknown function cosine -> correlation')
#
#    r.data('true_C', true_C).display('posneg', max_value=1).add_to(f, 'ground truth cosine matrix')
#    r.data('gt_dist', true_dist).display('scale').add_to(f, 'ground truth distance matrix')
#
#    
#    has_more = results['algo_class'] in [ CBCt, CBCt2]
#        
#    cols = 7
#    if has_more: cols += 2
#    fit = r.figure(cols=cols)
#    
#    for i, it in enumerate(iterations): 
#        rit = r.node('iteration%d' % i)
#        
#        def display_posneg(what, caption="no desc"):
#            data = it[what]
#            nid = what
#            n = rit.data(nid, data)
#            n.display('posneg', max_value=1)
#            fit.sub(n, caption=caption + ' (``%s``)' % what)
#
#        def display_coords(nid, coords, caption=None):    
#            n = rit.data(nid, coords)
#            with n.data_pylab('plot') as pylab:
#                plot_coords(pylab, coords)
#            fit.sub(n, caption=caption)
#        
#        display_coords('current_guess_for_S', it['current_guess_for_S'],
#                       'Current guess for coordinates.')
#        display_posneg('guess_for_C', 'Cosines corresponding to guess for S.')
#        display_posneg('new_estimated_C', 'Current guess for cosine matrix')
#        
#        if has_more:
#            display_posneg('dont_trust', 'Areas we do not trust.')
#            display_posneg('careful_C', 'The updated version of C.')
#        
#        
#        display_coords('new_guess_for_S', it['new_guess_for_S'],
#                       'New guess for coordinates (errors %.2f / %.2f deg)' % 
#                       (it['error_deg'], it['rel_error_deg']))
#        
#        new_C = cosines_from_directions(it['new_guess_for_S'])
#        with rit.data_pylab('r_vs_est_c') as pylab:
#            pylab.plot(new_C.flat, R.flat, '.', markersize=0.2)
#            pylab.xlabel('estimated cosine')
#            pylab.ylabel('correlation measure')
#            pylab.axis((-1, 1, -1, 1))
#        rit.last().add_to(fit, 'R vs current C') 
#        
#        new_C_order = scale_score(new_C)
#        with rit.data_pylab('r_order_vs_est_c_order') as pylab:
#            pylab.plot(new_C_order.flat, R_order.flat, '.', markersize=0.2)
#            pylab.xlabel('estimated cosine (order)')
#            pylab.ylabel('correlation measure (order)')
#        rit.last().add_to(fit, 'order comparison (spearman: %f robust: )' % 
#                            (it['spearman'], it['spearman_robust']))
#        
#        # if groundtruth
#        if true_S.shape[0] == 2:
#            with rit.data_pylab('theta_compare') as pylab:
#                true_theta = np.degrees(angles_from_directions(results['true_S']))
#                theta = np.degrees(angles_from_directions(it['S_aligned']))
#                theta = find_closest_multiple(theta, true_theta, 360)
#                pylab.plot(true_theta, theta, '.')
#                pylab.xlabel('true angles (deg)')
#                pylab.ylabel('estimated angles (deg)')
#                pylab.axis('equal')
#            fit.sub(rit.resolve_url('theta_compare'), 'True vs estimated angles.')
#
#        if False: # too fancy 
#            with rit.data_pylab('sol_compare') as pylab:
#                for i in range(len(theta)):
#                    pylab.plot([0, 1], [true_theta[i], theta[i]], '-')
#            fit.sub(rit.resolve_url('sol_compare'), 'Estimated (left) and true (right) angles.')
#
#    return r
#

        
def create_report_generic_iterations(results):
    ''' Black box plots for generic algorithm. '''
    r = Report('generic_iterations')

    R = results['R']
    true_S = results['true_S']
    twod = true_S.shape[0] == 2
    
    if twod:
        true_theta_deg = np.degrees(angles_from_directions(true_S))
    true_C = results['true_C']
    iterations = results['iterations']
    R_order = results['R_order']

    true_dist = distances_from_cosines(true_C)

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

    cols = 3
    if twod: cols += 1
    
    fit = r.figure(cols=cols)
    
    for i, it in enumerate(iterations): 
        S = it['S']
        S_aligned = it['S_aligned']
        error_deg = it['error_deg']
        rel_error_deg = it['rel_error_deg']
        C = cosines_from_directions(S)
        C_order = scale_score(C)
        if twod:
            theta_deg = np.degrees(angles_from_directions(S_aligned))
            theta_deg = find_closest_multiple(theta_deg, true_theta_deg, 360)

        rit = r.node('iteration%d' % i) 

        def display_coords(nid, coords, caption=None):    
            n = rit.data(nid, coords)
            with n.data_pylab('plot') as pylab:
                plot_coords(pylab, coords)
            fit.sub(n, caption=caption)
        
        display_coords('S', S,
                       'Guess for coordinates (errors %.2f / %.2f deg)' % 
                       (error_deg , rel_error_deg))
        
        with rit.data_pylab('r_vs_est_c') as pylab:
            pylab.plot(C.flat, R.flat, '.', markersize=0.2)
            pylab.xlabel('estimated cosine')
            pylab.ylabel('correlation measure')
#            pylab.axis((-1, 1, -1, 1))
        rit.last().add_to(fit, 'R vs current C') 

#        with rit.data_pylab('r_dot_vs_est_c_dot') as pylab:
#            order = C_order.astype('int')
#            Cdot = np.diff(C.flat[order])
#            Rdot = np.diff(R.flat[order])
#            ratio = np.log(Rdot) - np.log(Cdot)
#            pylab.plot(Cdot, ratio, '.', markersize=0.2)
#            pylab.xlabel('estimated dot cosine')
#            pylab.ylabel('ratio dot ')
##            pylab.axis((-1, 1, -1, 1))
#        rit.last().add_to(fit, 'R dot vs current C dot') 
        
        with rit.data_pylab('r_order_vs_est_c_order') as pylab:
            pylab.plot(C_order.flat, R_order.flat, '.', markersize=0.2)
            pylab.xlabel('estimated cosine (order)')
            pylab.ylabel('correlation measure (order)')
        rit.last().add_to(fit, 'order comparison (spearman: %f robust: %f)' % 
                            (it['spearman'], it['spearman_robust']))

        # if groundtruth
        if twod:
            with rit.data_pylab('theta_compare') as pylab:
                pylab.plot(true_theta_deg, true_theta_deg, 'k--')
                pylab.plot(true_theta_deg, theta_deg, '.')
                pylab.xlabel('true angles (deg)')
                pylab.ylabel('estimated angles (deg)')
                pylab.axis('equal')
            rit.last().add_to(fit, 'True vs estimated angles.')
          
    return r


def plot_coords(pylab, coords):
    pylab.plot(coords[0, :], coords[1, :], 'k-')
    pylab.plot(coords[0, :], coords[1, :], '.')
    pylab.axis('equal')

