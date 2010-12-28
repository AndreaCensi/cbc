from reprep import Report
from contracts.main import new_contract
from cbc.tools.natsort import natsorted

def create_report_comb_stats(comb_id, tc_ids, alg_ids, deps):

    r = Report(comb_id)
    
#    data, rlabels, clabels = algo_stats_A(results.values())
    
    data, rlabels, clabels = algo_stats_error_table(deps)
    
    r.table('stats', data, rows=rlabels, cols=clabels)
    
    return r


new_contract('header', 'None|str')
new_contract('table_desc', '''tuple(list[R](list[C]),list[R](header),list[C](header))''')

#@contracts(results='list(dict)', returns='table_desc')
#def algo_stats_A(results):
#    rows_labels = []
#    data = []
#    cols_labels = ['combination', 'average error (deg)']
#    for r in results:
#        row = [r['combid'],
#               "%.2f" % r['results']['error_deg']]
#        rows_labels.append(None)
#        data.append(row)
#        
#    return data, rows_labels, cols_labels 
    
def algo_stats_error_table(results):
    all_tc = natsorted(set([tc for tc, algo in results.keys()]), key=lambda x: str(x))
    all_algo = natsorted(set([algo for tc, algo in results.keys()]))

#    rows = [tc.tcid for tc in all_tc]
#    cols = ['%s-%s' % (algo[0].__name__, algo[1]) for algo in all_algo]
    rows = all_tc
    cols = all_algo
    
    def element(res):
        return '%.2f' % res['error_deg']
    
    data = [ [ element(results[(tc, algo)]) 
               for algo in all_algo ] 
             for tc in all_tc]
     
    return data, rows, cols        
