from nose.tools import nottest
import numpy as np
from reprep import Report

from ..tools import scale_score 
from .utils import plot_one_against_the_other, util_plot_euclidean_coords2d, \
    plot_and_display_coords

@nottest
def create_report_test_case(tcid, tc):
    r = Report('test_case-%s' % tcid)
    
    r.add_child(tc_problem_plots(tc)) 
    
    if tc.is_spherical() and tc.has_ground_truth:
        r.add_child(tc_ground_truth_plots_sph(tc))
    if tc.is_euclidean() and tc.has_ground_truth:
        r.add_child(tc_ground_truth_plots_euc(tc))
        
    return r

def tc_problem_plots(tc, rid='problem_data'):
    r = Report(rid)
    R = tc.R
    n = R.shape[0]
    # zero diagonal
    Rz = (1 - np.eye(n)) * R
    
    f = r.figure(cols=3)
    
    r.data("Rz", Rz).display('posneg')
    f.sub('Rz', caption='The given correlation matrix (diagonal set to 0)')
    
    return r
    
def tc_ground_truth_plots_sph(tc, rid='ground_truth'):
    r = Report(rid)
    assert tc.has_ground_truth
    
    cols = 5
    if tc.true_kernel is not None:
        cols += 1
    
    f = r.figure(cols=cols, caption='Ground truth plots.')


    plot_and_display_coords(r, f, 'true_S', tc.true_S)
#
#    with r.data('coordinates', tc.true_S).data_pylab('plot') as pylab:
#        plot_coords(pylab, tc.true_S)

    n = r.data('true_C', tc.true_C).display('posneg')  
    f.sub(n, 'Actual cosine matrix')
    
    n = r.data('true_D', tc.true_D).display('scale')  
    f.sub(n, 'Actual distance matrix')
    
    with r.data_pylab('linearity_func') as pylab:
        x = tc.true_C.flat
        y = tc.R.flat
        pylab.plot(x, y, '.', markersize=0.2)
        pylab.xlabel('true_C')
        pylab.ylabel('R')
    r.last().add_to(f, 'Relation (function)')
    
    n = plot_one_against_the_other(r, 'true_CvsR', tc.true_C, tc.R)
    f.sub(n, 'Relation (Sample histogram)')
    
    true_C_order = scale_score(tc.true_C)
    R_order = scale_score(tc.R)
    with r.data_pylab('linearity') as pylab:
        x = true_C_order.flat
        y = R_order.flat
        pylab.plot(x, y, '.', markersize=0.2)
        pylab.xlabel('true_C score')
        pylab.ylabel('R score')
        
    f.sub('linearity', 'Linearity plot (the closer this is to a line, the better '
                        'we can solve)')
    
    if tc.true_kernel is not None:
        x = np.linspace(-1, 1, 512)
        y = tc.true_kernel(x)
        with r.data_pylab('kernel') as pylab:
            pylab.plot(x, y)
            pylab.xlabel('cosine')
            pylab.ylabel('correlation')
            pylab.axis((-1, 1, -1, 1))
        f.sub('kernel', caption='Actual analytical kernel')
    
    return r


def tc_ground_truth_plots_euc(tc, rid='ground_truth'):
    r = Report(rid)
    assert tc.has_ground_truth
    
    cols = 4
    if tc.true_kernel is not None:
        cols += 1
    
    f = r.figure(cols=cols, caption='Ground truth plots.')

    util_plot_euclidean_coords2d(r, f, 'coordinates', tc.true_S)
 
    n = r.data('true_D', tc.true_D).display('scale')  
    f.sub(n, 'Actual distance matrix')
    
    with r.data_pylab('linearity_func') as pylab:
        x = tc.true_D.flat
        y = tc.R.flat
        pylab.plot(x, y, '.', markersize=0.2)
        pylab.xlabel('true_D')
        pylab.ylabel('R')
    r.last().add_to(f, 'Relation (function)')
    
    n = plot_one_against_the_other(r, 'true_DvsR', tc.true_D, tc.R)
    f.sub(n, 'Relation (Sample histogram)')
    
    true_D_order = scale_score(tc.true_D)
    R_order = scale_score(tc.R)
    with r.data_pylab('linearity') as pylab:
        x = true_D_order.flat
        y = R_order.flat
        pylab.plot(x, y, '.', markersize=0.2)
        pylab.xlabel('true_D score')
        pylab.ylabel('R score')
        
    f.sub('linearity', 'Linearity plot (the closer this is to a line, the better '
                        'we can solve)')
    
    if tc.true_kernel is not None:
        x = np.linspace(0, tc.true_D.max(), 512)
        y = tc.true_kernel(x)
        with r.data_pylab('kernel') as pylab:
            pylab.plot(x, y)
            pylab.xlabel('distance')
            pylab.ylabel('R')
#            pylab.axis((-1, 1, -1, 1))
        f.sub('kernel', caption='Actual analytical kernel')
    
    return r

