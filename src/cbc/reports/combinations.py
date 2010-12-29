import numpy as np

from reprep import Report

from ..tools import natsorted

def create_report_comb_stats(comb_id, tc_ids, alg_ids, deps):
    r = Report('set-%s' % comb_id)
    
    has_ground_truth = 'cheat' in alg_ids
    
    if has_ground_truth:
        for tc_id in tc_ids:
            max_spearman = deps[(tc_id, 'cheat')]['spearman']
            for alg_id in alg_ids:
                res = deps[(tc_id, alg_id)]
                res['spearman_score'] = res['spearman'] / max_spearman
    
    def tablevar(var, format='%.2f'):
        def getter(tc_id, alg_id):
            res = deps[(tc_id, alg_id)]
            return format % res[var]
        return getter

    if has_ground_truth:
        r.table('spearman_score', caption='Spearman correlation (normalized)',
            **generic_table(tc_ids, alg_ids, tablevar('spearman_score', '%.6f')))
    
    r.table('angles_corr', caption='Angle correlation',
            **generic_table(tc_ids, alg_ids, tablevar('angles_corr', '%.4f')))


    r.table('abs_error_deg', caption='Final average absolute error (deg)',
            **generic_table(tc_ids, alg_ids, tablevar('error_deg')))
    
    r.table('abs_rel_error_deg', caption='Final average relative error (deg)',
            **generic_table(tc_ids, alg_ids, tablevar('rel_error_deg')))

    r.table('spearman', caption='Spearman correlation',
            **generic_table(tc_ids, alg_ids, tablevar('spearman', '%.6f')))
    
    r.table('spearman_robust', caption='Spearman correlation',
            **generic_table(tc_ids, alg_ids, tablevar('spearman_robust', '%.6f')))

    r.table('diameter', caption='Diameter of solution',
            **generic_table(tc_ids, alg_ids, tablevar('diameter_deg', '%.1f')))


    for tc_id in tc_ids:
        rtc = r.node(tc_id)
        def variable(var):
            def get_trace(alg_id):
                res = deps[(tc_id, alg_id)]
                its = res['iterations']
                return [it[var] for it in its]
            return get_trace
            
        ftc = rtc.figure(cols=5, caption='Error per iteration')
        generic_iteration_plot(rtc, ftc, 'error_deg', alg_ids, variable('error_deg'),
                               caption='Absolute error')
        generic_iteration_plot(rtc, ftc, 'rel_error_deg', alg_ids, variable('rel_error_deg'),
                               caption='Relative error')
        generic_iteration_plot(rtc, ftc, 'spearman', alg_ids, variable('spearman'),
                               caption='Spearman correlation')
        generic_iteration_plot(rtc, ftc, 'spearman_robust', alg_ids,
                               variable('spearman_robust'),
                               caption='Spearman correlation (rob)')
        generic_iteration_plot(rtc, ftc, 'diameter', alg_ids, variable('diameter_deg'),
                               caption='Diameter of solution')
        generic_iteration_plot(rtc, ftc, 'angles_corr', alg_ids, variable('angles_corr'),
                               caption='Correlation of angles')
    
    return r
    
def generic_table(tc_ids, alg_ids, get_element, sorted=True):
    if sorted:
        tc_ids = natsorted(tc_ids)
        alg_ids = natsorted(alg_ids)
    
    rows = tc_ids
    cols = alg_ids
    
    make_row = lambda tc_id: [ get_element(tc_id, alg_id) for alg_id in alg_ids ]
    data = [  make_row(tc_id) for tc_id in tc_ids] 
     
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
                pylab.plot([0, max_trace_length], [trace, trace], '-', label=alg_id)
            else:
                pylab.plot(trace, 'x-', label=alg_id)
        pylab.legend()
        
    f.sub(report.last(), caption=caption)
    
    
    

#new_contract('header', 'None|str')
#new_contract('table_desc', '''tuple(list[R](list[C]),list[R](header),list[C](header))''')

