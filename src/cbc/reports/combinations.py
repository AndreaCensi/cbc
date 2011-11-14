from . import np, Report
from ..utils import natsorted


def create_report_comb_stats(comb_id, tc_ids, alg_ids, deps):
    r = Report('set-%s' % comb_id)
    
    has_ground_truth = 'cheat' in alg_ids or 'echeat' in alg_ids
    
    if 'cheat' in alg_ids: cheater = 'cheat'
    if 'echeat' in alg_ids: cheater = 'echeat'
     
    if has_ground_truth:
        for tc_id in tc_ids:
            max_spearman = deps[(tc_id, cheater)]['spearman']
            for alg_id in alg_ids:
                res = deps[(tc_id, alg_id)]
                res['spearman_score'] = res['spearman'] / max_spearman
    
    def tablevar(var, format='%.2f', not_found=np.NaN): #@ReservedAssignment
        def getter(tc_id, alg_id):
            res = deps[(tc_id, alg_id)]
            if var in res:
                return format % res[var]
            else:
#                return '/'
                return not_found
        return getter

    if has_ground_truth:
        r.table('spearman_score', caption='Spearman correlation (normalized)',
            **generic_table(tc_ids, alg_ids, tablevar('spearman_score', '%.4f')))

#    print deps.values()[0]['iterations'][0].keys()
    
    has_angles_corr = 'angles_corr' in  deps.values()[0]['iterations'][0]
    
    if has_angles_corr:
        r.table('angles_corr', caption='Angle correlation',
            **generic_table(tc_ids, alg_ids, tablevar('angles_corr', '%.4f')))
    
    r.table('abs_error_deg', caption='Final average absolute error (deg)',
            **generic_table(tc_ids, alg_ids, tablevar('error_deg')))
    
    r.table('abs_rel_error_deg', caption='Final average relative error (deg)',
            **generic_table(tc_ids, alg_ids, tablevar('rel_error_deg')))

    r.table('scaled_rel_error', caption='Final relative error (after scaling)',
            **generic_table(tc_ids, alg_ids, tablevar('scaled_rel_error', '%.4f')))
    r.table('scaled_error', caption='Final abs error (after scaling+ortho.)',
            **generic_table(tc_ids, alg_ids, tablevar('scaled_error', '%.4f')))


    r.table('spearman', caption='Spearman correlation',
            **generic_table(tc_ids, alg_ids, tablevar('spearman', '%.4f')))
    
    r.table('spearman_robust', caption='Spearman correlation (robust)',
            **generic_table(tc_ids, alg_ids, tablevar('spearman_robust', '%.4f')))

    r.table('diameter', caption='Diameter of solution',
            **generic_table(tc_ids, alg_ids, tablevar('diameter_deg', '%.1f')))

    r.table('phase', caption='Convergence phase',
            **generic_table(tc_ids, alg_ids, tablevar('phase', '%s'), mark_lower=False))

    plot_alg_ids = [x for x in alg_ids if x not in ['rand2d', 'rand3d']]

    for tc_id in tc_ids:
        rtc = r.node(tc_id)
        def variable(var, not_found=np.NaN):
            def get_trace(alg_id):
                res = deps[(tc_id, alg_id)]
                its = res['iterations']
                def getvar(it, var):
                    if var in it:
                        return it[var]
                    else: 
                        return not_found
                return [getvar(it, var) for it in its]
            return get_trace
            
        ftc = rtc.figure(cols=5, caption='Error per iteration')
        generic_iteration_plot(rtc, ftc, 'error_deg', plot_alg_ids, variable('error_deg'),
                               caption='Absolute error')
        generic_iteration_plot(rtc, ftc, 'rel_error_deg', plot_alg_ids, variable('rel_error_deg'),
                               caption='Relative error')
        
        generic_iteration_plot(rtc, ftc, 'scaled_rel_error', plot_alg_ids, variable('scaled_rel_error'),
                               caption='Relative error (after scaling)')

        generic_iteration_plot(rtc, ftc, 'spearman', plot_alg_ids, variable('spearman'),
                               caption='Spearman correlation')
        generic_iteration_plot(rtc, ftc, 'spearman_robust', plot_alg_ids,
                               variable('spearman_robust'),
                               caption='Spearman correlation (rob)')
        generic_iteration_plot(rtc, ftc, 'diameter', plot_alg_ids, variable('diameter_deg'),
                               caption='Diameter of solution')

        generic_iteration_plot(rtc, ftc, 'robust', plot_alg_ids, variable('robust'),
                               caption='robust')


        compared_iteration_plot(rtc, ftc, 'error_vs_spearman',
                                plot_alg_ids,
                                variable('spearman'),
                                variable('error_deg'),
                               caption='absolute error vs spearman')
        compared_iteration_plot(rtc, ftc, 'error_vs_spearman_robust',
                                plot_alg_ids,
                                variable('spearman_robust'),
                                variable('error_deg'),
                                caption='absolute error vs spearman_robust')
  

        compared_iteration_plot(rtc, ftc, 'error_vs_robust',
                                plot_alg_ids,
                                variable('robust'),
                                variable('error_deg'),
                                caption='absolute error vs robust')
        
        if has_angles_corr:
            generic_iteration_plot(rtc, ftc, 'angles_corr', plot_alg_ids,
                                   variable('angles_corr'),
                                   caption='Correlation of angles')
        
    
    return r
    
def generic_table(tc_ids, alg_ids, get_element,
                  sorted=True, mark_lower=True): #@ReservedAssignment
    if sorted:
        tc_ids = natsorted(tc_ids)
        alg_ids = natsorted(alg_ids)
    
    rows = tc_ids
    cols = alg_ids
    
    def make_row(tc_id):
        entries = [ get_element(tc_id, alg_id) for alg_id in alg_ids ]
        if mark_lower:
            # re-convert two numbers
            # do not consider these for the stats:
            avoid = ['rand2d', 'rand3d', 'cheat', 'echeat']
            values = [float(x) for (algo, x) in zip(alg_ids, entries)]
            selected = [float(x) for (algo, x) in zip(alg_ids, entries)
                        if algo not in avoid]
            values_max = max(selected)
            values_min = min(selected)
            for i in range(len(entries)):
                if alg_ids[i] in avoid: continue 
                if values[i] == values_max:
                    mark = '(H)'
                elif values[i] == values_min:
                    mark = '(L)'
                else:
                    mark = None
                if mark:
                    entries[i] = '%s %s' % (mark, entries[i])
                    
        return entries 
    
    data = [make_row(tc_id) for tc_id in tc_ids] 
     
    return dict(data=data, rows=rows, cols=cols)        


def generic_iteration_plot(report, f, nid, alg_ids, get_trace, caption=None):
    traces = []
    for alg_id in alg_ids:
        tr = get_trace(alg_id)
        tr = np.array(tr)
        traces.append(tr)
    
    max_trace_length = max(len(tr) for tr in traces)
    
    with report.data_pylab(nid) as pylab:
        for alg_id, trace in zip(alg_ids, traces):
            if len(trace) == 1:
                # one iteration, write continuous line
                pylab.plot([0, max_trace_length], [trace, trace],
                           '-', label=alg_id)
            else:
                pylab.plot(trace, 'x-', label=alg_id)
#        pylab.legend()
        
    f.sub(report.last(), caption=caption)
    

def compared_iteration_plot(report, f, nid, alg_ids, get_trace1, get_trace2,
                            caption=None):
    with report.data_pylab(nid) as pylab:
        for alg_id  in alg_ids:
            x = get_trace1(alg_id)
            y = get_trace2(alg_id)
            pylab.plot(x, y, 'x', label=alg_id)
#        pylab.legend()
        
    f.sub(report.last(), caption=caption)
     
