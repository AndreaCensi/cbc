import numpy as np

from reprep import Report 

from ..tools import (scale_score, find_closest_multiple,
                      euclidean_distances, distances_from_directions,
                     cosines_from_directions, angles_from_directions)
from ..algorithms import SPHERICAL, EUCLIDEAN
from . import util_plot_euclidean_coords2d, zero_diagonal, \
    plot_and_display_coords, add_order_comparison_figure, \
    util_plot_xy_generic, add_distance_vs_sim_figure


LABEL_D = 'distance'
LABEL_D_ORDER = 'order(distance)'
LABEL_TRUE_D_ORDER = 'order(true distance)'
LABEL_TRUE_D = 'order(true distance)'
LABEL_R = 'similarity'
LABEL_R_ORDER = 'order(similarity)'

def create_report_iterations(exc_id, results):
    r = Report(exc_id)
        
    has_ground_truth = 'true_S' in results and results['true_S'] is not None

    if results['geometry'] == SPHERICAL:
        if has_ground_truth:
            r.add_child(create_report_final_solution(results))
            r.add_child(create_report_generic_iterations(results))
        else:
            r.add_child(create_report_generic_iterations_observable(results))
            
    if results['geometry'] == EUCLIDEAN:
        if has_ground_truth:
            r.add_child(create_report_final_solution_euclidean(results))
            r.add_child(create_report_generic_iterations_euclidean(results))
#        else:
#            r.add_child(create_report_generic_iterations_observable_euclidean(results))
    return r


def create_report_final_solution(results):
    R = results['R']
    true_S = results['true_S']
    S_aligned = results['S_aligned']
    S = results['S']
    D = distances_from_directions(S)
    D_order = scale_score(-D) 
    true_D = distances_from_directions(true_S)
    true_D_order = scale_score(-true_D)
    R_order = scale_score(R)

    ########
    r = Report('final_solution')    
    f = r.figure('unobservable_measures',
                 caption='Comparisons with ground truth (unobservable)', cols=4)
    
    if S_aligned.shape[0] == 2:
        solutions_comparison_plots(r, f, true_S, S_aligned)
 
    util_plot_euclidean_coords2d(r, f, 'S_aligned', S)
    util_plot_euclidean_coords2d(r, f, 'true_S', true_S)

    f2 = r.figure('observable_measures', cols=3, caption='Computable measures')
     
    add_order_comparison_figure(r, 'D_order_vs_R_order', f2, 'Order comparison (results)',
                                D_order, R_order, LABEL_D_ORDER, LABEL_R_ORDER)
   
    add_order_comparison_figure(r, 'true_D_order_vs_R_order', f2,
                                'Order comparison (ground truth)',
                                true_D_order, R_order, LABEL_TRUE_D_ORDER, LABEL_R_ORDER)

    add_distance_vs_sim_figure(r, 'D_vs_R', f2, 'Kernel',
                                D, R, LABEL_D, LABEL_R)
    
    add_distance_vs_sim_figure(r, 'true_D_vs_R', f2, 'Kernel',
                                true_D, R, LABEL_TRUE_D, LABEL_R)

    return r
        
def create_report_final_solution_euclidean(results):
    R = results['R']
    S = results['S']
    D = euclidean_distances(S)
    true_S = results['true_S']
    true_D = euclidean_distances(true_S)
    R_order = scale_score(R)
    D_order = scale_score(-D)
    true_D_order = scale_score(-true_D)
    ndim = S.shape[0] 
    #########
    r = Report('final_solution')
    
    f = r.figure('unobservable_measures',
                 caption='Comparisons with ground truth (unobservable)', cols=4)
    
    if ndim == 2: 
        util_plot_euclidean_coords2d(r, f, 'S_aligned', S)
        util_plot_euclidean_coords2d(r, f, 'true_S', true_S)
                
    f2 = r.figure('order comparisons', cols=3)

    add_order_comparison_figure(r, 'D_order_vs_R_order', f2, 'Order comparison (results)',
                                D_order, R_order, LABEL_D_ORDER, LABEL_R_ORDER)
   
    add_order_comparison_figure(r, 'true_D_order_vs_R_order', f2, 'Order comparison (ground truth)',
                                true_D_order, R_order, LABEL_TRUE_D_ORDER, LABEL_R_ORDER)
    
    add_distance_vs_sim_figure(r, 'D_vs_R', f2, 'Kernel',
                                D, R, LABEL_D, LABEL_R)
    add_distance_vs_sim_figure(r, 'true_D_vs_R', f2, 'Kernel',
                                true_D, R, LABEL_TRUE_D, LABEL_R)
    
    return r


def solutions_comparison_plots(r, f, true_S, S_aligned):
    true_theta = np.degrees(angles_from_directions(true_S))
    theta = np.degrees(angles_from_directions(S_aligned))
    theta = find_closest_multiple(theta, true_theta, 360)
    #########
#    plot_and_display_coords(r, f, 'true_S', true_S, 'Ground truth')
#    plot_and_display_coords(r, f, 'S_aligned', S_aligned, 'Solution, aligned')

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
         

def create_report_generic_iterations(results):
    ''' Black box plots for generic algorithm. '''
    R = results['R']
    true_S = results['true_S']
    ndim = true_S.shape[0]
    true_C = cosines_from_directions(true_S)
    true_dist = distances_from_directions(true_S)
    iterations = results['iterations']
    R_order = scale_score(R)
    #######
    r = Report('generic_iterations')
    if ndim == 2:
        true_theta_deg = np.degrees(angles_from_directions(true_S))

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
    if ndim == 2: cols += 1
    
    fit = r.figure(cols=cols)
    
    for i, it in enumerate(iterations): 
        S = it['S']
        D = distances_from_directions(S)
        D_order = scale_score(-D)
        S_aligned = it['S_aligned']
        error_deg = it['error_deg']
        rel_error_deg = it['rel_error_deg']
#        C = cosines_from_directions(S)
#        C_order = scale_score(C)
        if ndim == 2:
            theta_deg = np.degrees(angles_from_directions(S_aligned))
            theta_deg = find_closest_multiple(theta_deg, true_theta_deg, 360)

        rit = r.node('iteration%d' % i) 

        plot_and_display_coords(rit, fit, 'S', S,
                                'Guess for coordinates (errors %.2f / %.2f deg)' % 
                                (error_deg , rel_error_deg))
#        
#        def display_coords(nid, coords, caption=None):    
#            n = rit.data(nid, coords)
#            with n.data_pylab('plot') as pylab:
#                plot_coords(pylab, coords)
#            fit.sub(n, caption=caption)
#        
#        display_coords('S', S,
#                       'Guess for coordinates (errors %.2f / %.2f deg)' % 
#                       (error_deg , rel_error_deg))
        
        add_order_comparison_figure(rit, 'D_order_vs_R_order', fit,
                                    'Order comparison (results)',
                                D_order, R_order, LABEL_D_ORDER, LABEL_R_ORDER)

        add_distance_vs_sim_figure(rit, 'D_vs_R', fit, 'Kernel',
                                D, R, LABEL_D, LABEL_R)

#
#        with rit.data_pylab('r_vs_est_c') as pylab:
#            pylab.plot(C.flat, R.flat, '.', markersize=0.2)
#            pylab.xlabel('estimated cosine')
#            pylab.ylabel('correlation measure')
##            pylab.axis((-1, 1, -1, 1))
#        rit.last().add_to(fit, 'R vs current C') 
 
#        with rit.data_pylab('r_order_vs_est_c_order') as pylab:
#            pylab.plot(C_order.flat, R_order.flat, '.', markersize=0.2)
#            pylab.xlabel('estimated cosine (order)')
#            pylab.ylabel('correlation measure (order)')
#        rit.last().add_to(fit, 'order comparison (spearman: %f robust: %f)' % 
#                            (it['spearman'], it['spearman_robust']))

        # if groundtruth
        if ndim == 2:
            with rit.data_pylab('theta_compare') as pylab:
                pylab.plot(true_theta_deg, true_theta_deg, 'k--')
                pylab.plot(true_theta_deg, theta_deg, '.')
                pylab.xlabel('true angles (deg)')
                pylab.ylabel('estimated angles (deg)')
                pylab.axis('equal')
            rit.last().add_to(fit, 'True vs estimated angles.')
          
    return r



def create_report_generic_iterations_euclidean(results):
    ''' Black box plots for generic algorithm. '''
    R = results['R']
    true_S = results['true_S'] 
    true_D = euclidean_distances(true_S)

    true_D_order = scale_score(-true_D)
    iterations = results['iterations']
    R_order = scale_score(R)
    #######
    
    r = Report('generic_iterations')
    
    f = r.figure(cols=3, caption='Data and ground truth')
    f.data('R', R).display('posneg', max_value=1).add_to(f, 'Given R')
    f.data('R0', zero_diagonal(R)).display('posneg', max_value=1).\
        add_to(f, 'Given R (diagonal set to 0).')
    
    r.data('R_order', R_order).display('scale').add_to(f, 'Order for R')
    
    util_plot_xy_generic(r=r, f=f, nid='true_D_vs_R', x=true_D.flat, y=R.flat,
                        xlabel=LABEL_TRUE_D, ylabel=LABEL_R,
                         caption='Unknown function distance -> correlation')
    util_plot_xy_generic(r=r, f=f, nid='true_D_order_vs_R_order',
                         x=true_D_order.flat, y=R_order.flat,
                         xlabel=LABEL_TRUE_D_ORDER, ylabel=LABEL_R_ORDER,
                         caption='Distance Oderd vs Correlation order')

    fit = r.figure(cols=3)
    
    for i, it in enumerate(iterations): 
        S = it['S']
        D = euclidean_distances(S)
        D_order = scale_score(D) 

        rit = r.node('iteration%d' % i) 

        plot_and_display_coords(rit, fit, 'S', S, 'Guess for coordinates')

        # TODO: add aligned
        
#        util_plot_xy_generic(r=rit, f=fit, nid='D[i]_vs_R', x=D.flat, y=R.flat,
#                         xlabel='distance (k=%d)' % i, ylabel='correlation',
#                         caption='Unknown function distance -> correlation')
#        util_plot_xy_generic(r=rit, f=fit, nid='D[i]_order_vs_R_order',
#                         x=D_order.flat, y=R_order.flat,
#                         xlabel='distance order (k=%d)' % i, ylabel='correlation',
#                         caption='Distance Order vs Correlation order')

        add_order_comparison_figure(rit, 'D_order_vs_R_order', fit,
                                    'Order comparison (results)',
                                D_order, R_order, LABEL_D_ORDER, LABEL_R_ORDER)

        add_distance_vs_sim_figure(rit, 'D_vs_R', fit, 'Kernel',
                                D, R, LABEL_D, LABEL_R)

    return r



def create_report_generic_iterations_observable(results):
    r = Report('generic_iterations_observable')
    R = results['R']
    R_order = scale_score(R)

    iterations = results['iterations']


    f = r.figure(cols=3, caption='Data and ground truth')
    f.data('R', R).display('posneg', max_value=1).add_to(f, 'Given R')
    f.data('R0', zero_diagonal(R)).display('posneg', max_value=1).\
        add_to(f, 'Given R (diagonal set to 0).')
    
    r.data('R_order', R_order).display('scale').add_to(f, 'Order for R')
     
    cols = 3 
    
    fit = r.figure(cols=cols)
    
    for i, it in enumerate(iterations): 
        S = it['S']
        C = cosines_from_directions(S)
        C_order = scale_score(C)
        rit = r.node('iteration%d' % i) 

#        def display_coords(nid, coords, caption=None):    
#            n = rit.data(nid, coords)
#            with n.data_pylab('plot') as pylab:
#                plot_coords(pylab, coords)
#            fit.sub(n, caption=caption)
#        display_coords('S', S,
#                       'Guess for coordinates')
        
        
        plot_and_display_coords(rit, fit, 'S', S, 'Guess for coordinates')
#        
        
        with rit.data_pylab('r_vs_est_c') as pylab:
            pylab.plot(C.flat, R.flat, '.', markersize=0.2)
            pylab.xlabel('estimated cosine')
            pylab.ylabel('correlation measure')
#            pylab.axis((-1, 1, -1, 1))
        rit.last().add_to(fit, 'R vs current C') 
 
        with rit.data_pylab('r_order_vs_est_c_order') as pylab:
            pylab.plot(C_order.flat, R_order.flat, '.', markersize=0.2)
            pylab.xlabel('estimated cosine (order)')
            pylab.ylabel('correlation measure (order)')
        rit.last().add_to(fit, 'order comparison (spearman: %f robust: %f)' % 
                            (it['spearman'], it['spearman_robust']))
          
    return r


