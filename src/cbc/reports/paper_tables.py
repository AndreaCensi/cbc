import os
from reprep.out.platex import Latex
import numpy as np

tex_algo = [
    ('cheat', '\\oracle'),
    ('echeat', '\\oracle'),
    ('emds2', '\\eMDS'),
    ('embed2', '\\sMDS'),
    ('embed3', '\\sMDS'),
    #('CBC2d', '\\SBSE'),
    ('eCBC2d', '\\SBSE'),
    ('CBC2d', '\\SBSE'),
    ('CBC3d', '\\SBSE'),
    ('eCBC3d', '\\SBSE'),
    ('eCBC3dw', '\\SBSEw'),
    ('CBC3dw', '\\SBSEw'),
    ('CBC2dw', '\\SBSEw'),
    #('CBC3d', '\\SBSE'),
    ('CBC3dr50', '\\SBSEr'),
    ('CBC2dr10', '\\SBSEr'),
    ('CBC2dr50', '\\SBSEr'),
    ('CBC3dr50w', '\\SBSErw'),
    ('CBC2dr50w', '\\SBSErw'),
    ('CBC2dr10w', '\\SBSErw'),
]
#    
# nips_euclidean = ['emds2', 'echeat', 'eCBC2d']
#    nips_spherical2d = ['embed2', 'cheat', 'CBC2d', 'CBC2dw', 'CBC2dr50']
#    nips_spherical3d = ['embed3', 'cheat', 'CBC3d', 'CBC3dw']

def tc(dim, fov_deg, func, noise):
    dim = {2:"$\\Sone$", 3:"$\\Stwo$"}[dim]
    return '\\tc{%s}{%d}{\\%s}{\\%s}' % (dim, fov_deg, func, noise)

def tce(dim, kind, num, func, noise):
#%    return 'Euclidean %s %s %s %s %s' % (dim, kind, num, func, noise)
    dim = "$\\mathbb{R}^%s$" % dim
    return '\\tce{%s}{%d}{\\%s}' % (dim, num, func)

def sicktc(which, quantity):
    which = {0:'front', 1:'rear', 2:'both'}[which]
    #if which == 'front' and quantity != 'yinfsim':
    if quantity != 'yinfsim':
        return "\\sicktcb{\\%s}{\\%s}" % (which, quantity)
    else:
        return "\\sicktc{\\%s}{\\%s}" % (which, quantity)

tex_tc = [
 ('sick_front-y_infsim', sicktc(0, 'yinfsim')),
 ('sick_front-y_corr', sicktc(0, 'ycorr')),
 ('sick_front-y_dot_corr', sicktc(0, 'ydotcorr')),
 ('sick_front-y_dot_abs_corr', sicktc(0, 'ydotabscorr')),
 ('sick_front-y_dot_sign_corr', sicktc(0, 'ydotsigncorr')),
 ('sick_front-max', sicktc(0, 'scoremax'), 0),
 ('sick_front-mix', sicktc(0, 'scoremix')),
 
 ('sick_rear-y_infsim', sicktc(1, 'yinfsim'), 0),
 ('sick_rear-y_corr', sicktc(1, 'ycorr'), 0),
 ('sick_rear-y_dot_corr', sicktc(1, 'ydotcorr'), 0),
 ('sick_rear-y_dot_abs_corr', sicktc(1, 'ydotabscorr'), 0),
 ('sick_rear-y_dot_sign_corr', sicktc(1, 'ydotsigncorr'), 0),
 ('sick_rear-max', sicktc(1, 'scoremax'), 0),
 ('sick_rear-mix', sicktc(1, 'scoremix')),

 ('sick_both-y_infsim', sicktc(2, 'yinfsim'), 0),
 ('sick_both-y_corr', sicktc(2, 'ycorr'), 0),
 ('sick_both-y_dot_corr', sicktc(2, 'ydotcorr'), 0),
 ('sick_both-y_dot_abs_corr', sicktc(2, 'ydotabscorr'), 0),
 ('sick_both-y_dot_sign_corr', sicktc(2, 'ydotsigncorr'), 0),
 ('sick_both-max', sicktc(2, 'scoremax'), 0),
 ('sick_both-mix', sicktc(2, 'scoremix'), 0),
 
]

tex_tc.extend([
    ('mino4_grid24-y_corr', '\\tcCameraGrid'),
    ('mino4_midcen-y_corr', '\\tcCameraCross'),
    ('mino4_center-y_corr', '\\tcCameraCenter'),
    ('mino4_centerart-y_corr', '\\tcCameraCenterArt'),
])

tex_tc.extend([
    ('E2-grid-n180-eu_pow3', tce(2, 'grid', 180, 'powa', '')),
    ('E2-grid-n180-eu_pow7', tce(2, 'grid', 180, 'powb', '')),
    ('E2-grid-n180-eu_linear01', tce(2, 'grid', 180, 'lin', ''))
])

for noise in ['zero', 'noisy']:
    tex_tc.extend([
    ('rand-3D-fov45-pow3_sat-%s' % noise , tc(3, 45, 'powa', noise)) ,
    ('rand-3D-fov45-pow7_sat-%s' % noise , tc(3, 45, 'powb', noise)) ,
    ('rand-3D-fov45-linear01-%s' % noise , tc(3, 45, 'lin', noise)),
    ('rand-3D-fov90-pow3_sat-%s' % noise , tc(3, 90, 'powa', noise), 0),
    ('rand-3D-fov90-pow7_sat-%s' % noise , tc(3, 90, 'powb', noise), 0),
    ('rand-3D-fov90-linear01-%s' % noise , tc(3, 90, 'lin', noise), 0),
    ('rand-3D-fov270-pow3_sat-%s' % noise , tc(3, 270, 'powa', noise), 0),
    ('rand-3D-fov270-pow7_sat-%s' % noise , tc(3, 270, 'powb', noise)),
    ('rand-3D-fov270-linear01-%s' % noise , tc(3, 270, 'lin', noise)),
    ('rand-3D-fov360-pow3_sat-%s' % noise , tc(3, 360, 'powa', noise), 0),
    ('rand-3D-fov360-pow7_sat-%s' % noise , tc(3, 360, 'powb', noise), 0),
    ('rand-3D-fov360-linear01-%s' % noise , tc(3, 360, 'lin', noise), 0),
    
    ('rand-2D-fov270-pow3_sat-%s' % noise , tc(2, 270, 'powa', noise), 0),
    ('rand-2D-fov270-pow7_sat-%s' % noise , tc(2, 270, 'powb', noise), 0),
    ('rand-2D-fov270-linear01-%s' % noise , tc(2, 270, 'lin', noise), 0),
    ('rand-2D-fov315-pow3_sat-%s' % noise , tc(2, 315, 'powa', noise)),
    ('rand-2D-fov315-pow7_sat-%s' % noise , tc(2, 315, 'powb', noise)),
    ('rand-2D-fov315-linear01-%s' % noise , tc(2, 315, 'lin', noise)),
    ('rand-2D-fov360-pow3_sat-%s' % noise , tc(2, 360, 'powa', noise), 0),
    ('rand-2D-fov360-pow7_sat-%s' % noise , tc(2, 360, 'powb', noise)),
    ('rand-2D-fov360-linear01-%s' % noise , tc(2, 360, 'lin', noise)),
     
    ('rand-2D-fov45-pow3_sat-%s' % noise , tc(2, 45, 'powa', noise)),
    ('rand-2D-fov45-pow7_sat-%s' % noise , tc(2, 45, 'powb', noise)),
    ('rand-2D-fov45-linear01-%s' % noise , tc(2, 45, 'lin', noise)),
    ('rand-2D-fov90-pow3_sat-%s' % noise , tc(2, 90, 'powa', noise), 0),
    ('rand-2D-fov90-pow7_sat-%s' % noise , tc(2, 90, 'powb', noise)),
    ('rand-2D-fov90-linear01-%s' % noise , tc(2, 90, 'lin', noise)),
    
    ('rand-2D-fov315-pow3f-%s' % noise , tc(2, 315, 'powaf', noise)),
    ('rand-2D-fov315-pow7f-%s' % noise , tc(2, 315, 'powbf', noise))
])

tex_tc.append(('fly', '\\flydataset'))

for i in range(len(tex_tc)):
    tup = tex_tc[i]
    if len(tup) == 2:
        tex_tc[i] = (tup[0], tup[1], 1)

tex_tc = [ (a, b) for (a, b, c) in tex_tc if c >= 0]
table_dir = '~/rss/tables_all'

def create_tables_for_paper(comb_id, tc_ids, alg_ids, deps):
    print('Creating table for set %r' % comb_id)
    print('   tc: %r' % tc_ids)
    print(' algo: %r' % alg_ids)
    has_ground_truth = 'cheat' in alg_ids or 'echeat' in alg_ids
    
    if 'cheat' in alg_ids: cheater = 'cheat'
    if 'echeat' in alg_ids: cheater = 'echeat'

    if has_ground_truth:
        for tc_id in tc_ids:
            max_spearman = deps[(tc_id, cheater)]['spearman']
            for alg_id in alg_ids:
                res = deps[(tc_id, alg_id)]
                res['spearman_score'] = res['spearman'] / max_spearman
    
    def tablevar(var, format='%.2f', not_found=np.NaN):
        def getter(tc_id, alg_id):
            res = deps[(tc_id, alg_id)]
            if var in res:
                return format % res[var]
            else:
                return not_found
        return getter

    if has_ground_truth:
        write_table(comb_id, 'spearn',
            **generic_table(tc_ids, alg_ids, tablevar('spearman_score', '%.4f')))

    has_angles_corr = 'angles_corr' in  deps.values()[0]['iterations'][0]
    
    if has_angles_corr:
        write_table(comb_id, 'angcorr',
            **generic_table(tc_ids, alg_ids, tablevar('angles_corr', '%.4f')))
    
    
    write_table(comb_id, 'spear',
            **generic_table(tc_ids, alg_ids, tablevar('spearman', '%.4f')))
    
    write_table(comb_id, 'diameter',
            **generic_table(tc_ids, alg_ids, tablevar('diameter_deg', '%.2f'), sign=0))
    
#    write_table(comb_id, 'abs_rel_error_deg',
#            **generic_table(tc_ids, alg_ids, tablevar('abs_rel_error_deg', '%.4f'), sign=0))
    
    write_table(comb_id, 'procustes_deg',
            **generic_table(tc_ids, alg_ids, tablevar('error_deg', '%.2f'), sign= -1))
    
    write_table(comb_id, 'procustes',
            **generic_table(tc_ids, alg_ids, tablevar('error'), sign= -1))

    write_table(comb_id, 'rel_error',
            **generic_table(tc_ids, alg_ids, tablevar('rel_error', '%.4f'), sign=0))

    write_table(comb_id, 'rel_error_deg',
            **generic_table(tc_ids, alg_ids, tablevar('rel_error_deg', '%.2f'), sign=0))
    
    write_table(comb_id, 'scaled_error',
            **generic_table(tc_ids, alg_ids, tablevar('scaled_error', '%.4f'), sign=0))

    write_table(comb_id, 'scaled_error_deg',
            **generic_table(tc_ids, alg_ids, tablevar('scaled_error_deg', '%.2f'), sign=0))
    
    write_table(comb_id, 'scaled_rel_error_deg',
            **generic_table(tc_ids, alg_ids, tablevar('scaled_rel_error_deg', '%.2f'), sign=0))
    
    
def write_table(comb_id, table_id, data, rows, cols):
    
    directory = os.path.expanduser('%s/%s/' % (table_dir, comb_id))
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    filename = os.path.join(directory, '%s.tex' % table_id)
    print('Writing table to %r.' % filename)
    with Latex.fragment(filename, directory) as fragment:
        fragment.tabular_simple(data, row_desc=rows, col_desc=cols)

    filename = os.path.join(directory, '%s_nohead.tex' % table_id)
    print('Writing table to %r.' % filename)
    with Latex.fragment(filename, directory) as fragment:
        fragment.tabular_simple(data, row_desc=rows, col_desc=cols, write_col_desc=False)

    
def generic_table(tc_ids, alg_ids, get_element, sorted=True, mark_lower=True, sign= +1):
    named_tcs = [id for id, string in tex_tc] #@UnusedVariable
    named_algos = [id for id, string in tex_algo] #@UnusedVariable
    for tc_id in tc_ids:
        if not tc_id in named_tcs:
            print('Warning: cannot find TeX name for test case %r' % tc_id)
    for alg_id in alg_ids:
        if not alg_id in named_algos:
            print('Warning: cannot  find TeX name for algo  %r' % alg_id)

    # Only select the one we care and in the right order 
    tc_ids = [tc_id for tc_id, tex_string in tex_tc if tc_id in tc_ids] #@UnusedVariable
    alg_ids = [alg_id for alg_id, tex_string in tex_algo if alg_id in alg_ids] #@UnusedVariable
        
    print('Using only test cases: %r' % tc_ids)
    print('Using only algorithms: %r' % alg_ids)
    rows = [dict(tex_tc)[tc_id] for tc_id in tc_ids]
    cols = [dict(tex_algo)[alg_id] for alg_id in alg_ids]
    
    if 'cheat' in alg_ids: cheater = 'cheat'
    if 'echeat' in alg_ids: cheater = 'echeat'
    
    def make_row(tc_id):
        entries = [ get_element(tc_id, alg_id) for alg_id in alg_ids ]
        if mark_lower:
            # re-convert two numbers
            # do not consider these for the stats:
            avoid = ['rand2d', 'rand3d', 'cheat', 'echeat']
            if sign in [+1, -1]:
                values = [sign * float(x) for (algo, x) in zip(alg_ids, entries)]
                selected = [sign * float(x) for (algo, x) in zip(alg_ids, entries)
                            if algo not in avoid]
                values_max = max(selected)
                values_min = min(selected)
            else:
                reference = dict(zip(alg_ids, entries))[cheater]
                f = lambda x: np.abs(float(reference) - float(x))  
                values = [ f(x) for (algo, x) in zip(alg_ids, entries)]
                selected = [f(x) for (algo, x) in zip(alg_ids, entries)
                            if algo not in avoid]
                values_max = min(selected)
                values_min = max(selected)
                
            for i in range(len(entries)):
                if alg_ids[i] in avoid: continue 
                if values[i] == values_max:
                    mark = 'markbest'
                elif values[i] == values_min:
                    mark = 'markworst'
                else:
                    mark = None
                if mark:
                    entries[i] = '\\%s{%s}' % (mark, entries[i])
                    
        return entries 
    
    data = [make_row(tc_id) for tc_id in tc_ids] 
     
    return dict(data=data, rows=rows, cols=cols)        

 
 
