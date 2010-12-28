from reprep import Report

from ..tools import natsorted

def create_report_comb_stats(comb_id, tc_ids, alg_ids, deps):
    r = Report(comb_id)
    
    def el_error_deg(tc_id, alg_id):
        res = deps[(tc_id, alg_id)]
        return '%.2f' % res['error_deg']
    
    def el_rel_error_deg(tc_id, alg_id):
        res = deps[(tc_id, alg_id)]
        return '%.2f' % res['rel_error_deg']

    
    r.table('abs_error_deg', caption='Final average absolute error (deg)',
            **generic_table(tc_ids, alg_ids, el_error_deg))
    
    r.table('abs_rel_error_deg', caption='Final average relative error (deg)',
            **generic_table(tc_ids, alg_ids, el_rel_error_deg))

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


#new_contract('header', 'None|str')
#new_contract('table_desc', '''tuple(list[R](list[C]),list[R](header),list[C](header))''')

