from . import (nottest, np, Report, plot_one_against_the_other,
    util_plot_euclidean_coords2d, plot_and_display_coords,
    add_order_comparison_figure, util_plot_xy_generic)
from ..tc import CalibTestCase
from ..tools import scale_score


@nottest
def create_report_test_case(tcid, tc):
    assert isinstance(tcid, str)
    assert isinstance(tc, CalibTestCase), (type(tc), str(tc))

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
    true_C_order = scale_score(tc.true_C)
    R_order = scale_score(tc.R)

    r = Report(rid)
    assert tc.has_ground_truth

    cols = 5
    if tc.true_kernel is not None:
        cols += 1

    f = r.figure(cols=cols, caption='Ground truth plots.')

    plot_and_display_coords(r, f, 'true_S', tc.true_S)
#
#    with r.data('coordinates', tc.true_S).plot('plot') as pylab:
#        plot_coords(pylab, tc.true_S)

    n = r.data('true_C', tc.true_C).display('posneg')
    f.sub(n, 'Actual cosine matrix')

    n = r.data('true_D', tc.true_D).display('scale')
    f.sub(n, 'Actual distance matrix')

    util_plot_xy_generic(r, f, 'linearity_func',
                          tc.true_C.flat,
                          tc.R.flat, 'true_C', 'R',
                          caption='Relation (function)')

    n = plot_one_against_the_other(r, 'true_CvsR', tc.true_C, tc.R)
    f.sub(n, 'Relation (Sample histogram)')

    add_order_comparison_figure(r, 'linearity', f,
                'Linearity plot (the closer this is to a line, the better '
                'we can solve)', true_C_order, R_order,
                        'true_C', 'R')

    if tc.true_kernel is not None:
        x = np.linspace(-1, 1, 512)
        y = tc.true_kernel(x)
        with r.plot('kernel') as pylab:
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

    # TODO: change these to standard
    with r.plot('linearity_func') as pylab:
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
    with r.plot('linearity') as pylab:
        x = true_D_order.flat
        y = R_order.flat
        pylab.plot(x, y, '.', markersize=0.2)
        pylab.xlabel('true_D score')
        pylab.ylabel('R score')

    f.sub('linearity', 'Linearity plot (the closer this is to a line,'
                        ' the better we can solve)')

    if tc.true_kernel is not None:
        x = np.linspace(0, tc.true_D.max(), 512)
        y = tc.true_kernel(x)
        with r.plot('kernel') as pylab:
            pylab.plot(x, y)
            pylab.xlabel('distance')
            pylab.ylabel('R')
            pylab.axis((x.min(), x.max(), y.min(), y.max()))
        f.sub('kernel', caption='Actual analytical kernel')

    return r

