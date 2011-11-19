from .. import comp, compmake_console, batch_command, use_filesystem, np
from ..algorithms import get_list_of_algorithms
from ..configuration import TCConfig
from ..reports import (create_report_test_case, create_report_comb_stats,
    create_report_iterations, create_tables_for_paper)
from ..tc import CalibTestCase, get_syntethic_test_cases, get_real_test_cases
from ..tc.fly import get_fly_testcase
from ..tc.io.load import tc_load_spec
from ..tc.mino import get_mino_testcases
from ..tc.synthetic_euclidean import get_euclidean_test_cases
from ..tools import align_distributions
from ..utils import expand_string, make_sure_dir_exists
from .combinations import get_list_of_combinations
from contracts import check, disable_all
from optparse import OptionParser, OptionGroup
import datetime
import itertools
import os


join = os.path.join
# cbc_main --data_sick cbc_submission_data/sick.pickle \                                            
#          --data_fly  cbc_submission_data/fly.pickle \
#          --set 'paper*'  \
#          --outdir cbc_main_output
             
             
             
def main():
    parser = OptionParser()

    group = OptionGroup(parser, "Files and directories")

    group.add_option("--outdir",
                      help='Directory with variables.pickle and where '
                           'the output will be placed.')

#    group.add_option("--testdir", default=None)

    group.add_option("--data_sick", default=None,
                     help='.pickle file containing Sick data.')
    group.add_option("--data_mino", default=None,
                     help='directory containing Mino data.')
    group.add_option("--data_fly", default=None,
                     help='.pickle file containing fly simulation data.')
   
    group.add_option("--test_cases", default=None,
                    help='Base dire for test cases.')
 
    parser.add_option_group(group)

    group = OptionGroup(parser, "Experiments options")

    group.add_option("--contracts", default=False, action='store_true',
                      help='Enables PyContacts sanity checks.')
    
    group.add_option("--set", default='*',
                      help='[= %default] Which combinations to run.')

    group.add_option("--seed", default=None, type='int',
                      help='[= %default] Seed for random number generator.')
    
    parser.add_option_group(group)

    group = OptionGroup(parser, "Compmake options")

    group.add_option("--remake", default=False, action='store_true',
                      help='Remakes all (non interactive).')

    group.add_option("--report", default=False, action='store_true',
                      help='Cleans and redoes all reports (non interactive).')

    group.add_option("--report_stats", default=False, action='store_true',
                      help='Cleans and redoes the reports for the stats. (non interactive)')

    parser.add_option_group(group)

    (options, args) = parser.parse_args() #@UnusedVariable
    
    
    np.random.seed(options.seed)    
    
    if not options.contracts:
        disable_all()

    
    assert options.outdir is not None 
    
    available_test_cases = {}

    if options.test_cases is not None:
        TCConfig.load(options.test_cases)
    
        for tc_id in TCConfig.test_cases:
            available_test_cases[tc_id] = \
                (tc_load_spec, {'spec': TCConfig.test_cases[tc_id]})
            
    print('Generating synthetic test cases...')
    synthetic = get_syntethic_test_cases()
    available_test_cases.update(synthetic)
    
    euclidean = get_euclidean_test_cases()
    available_test_cases.update(euclidean)
    
#    if options.testdir is not None:
#        available_test_cases.update(standard_test_dir(options.testdir))
    
    if options.data_sick is not None:
        print('Preparing Sick data...')
        real = get_real_test_cases(options.data_sick)
        available_test_cases.update(real)
    
    if options.data_fly is not None:
        print('Preparing fly data...')
        available_test_cases.update(get_fly_testcase(options.data_fly))
    
    if options.data_mino is not None:
        print('Preparing Mino data...')
        available_test_cases.update(get_mino_testcases(options.data_mino))
        
    check('dict(str: tuple(Callable, dict))', available_test_cases)


    print('Creating list of algorithms..')
    algorithms = get_list_of_algorithms()    
    check('dict(str: tuple(Callable, dict))', algorithms)
    
    print('Creating list of combinations..')
    combinations = get_list_of_combinations()
    
    
    which = expand_string(options.set, list(combinations.keys()))
    print('I will use the sets: %s' % which)
    if len(which) == 1:    
        compmake_storage = join(options.outdir, 'compmake', which[0])
    else:
        compmake_storage = join(options.outdir, 'compmake', 'common_storage')
    
    use_filesystem(compmake_storage)


    print('Available %d test cases and %d algorithms' % 
          (len(available_test_cases), len(algorithms)))
    
    print('Staging creation of test cases reports')
    test_cases = {}
    test_case_reports = {} 
    def stage_test_case_report(tcid):
        if not tcid in available_test_cases:
            msg = ('Could not find test case %r \n %s' % 
                   (tcid, available_test_cases.keys()))
            raise Exception(msg)
        if not tcid in test_cases:
            f, args = available_test_cases[tcid]
            
            job_id = 'test_case_data-%s' % tcid
            test_cases[tcid] = comp(test_case_generate, f=f,
                                    args=args, job_id=job_id)
        
        if not tcid in  test_case_reports:
            job_id = 'test_case-%s-report' % tcid
            report = comp(create_report_test_case,
                          tcid, test_cases[tcid], job_id=job_id)
            job_id += '-write'
            filename = join(options.outdir, 'test_cases', '%s.html' % tcid)
            comp(write_report, report, filename, job_id=job_id)
            test_case_reports[tcid] = report
        return test_case_reports[tcid]
    
    # set of tuple (algo, test_case)
    executions = {}
    def stage_execution(tcid, algid):
        exc_id = '%s-%s' % (tcid, algid)
        stage_test_case_report(tcid)
        
        key = (tcid, algid)
        if not key in executions:
            test_case = test_cases[tcid]
            if not algid in algorithms:
                raise Exception('No %r known in %s' % (algid, algorithms.keys()))
            algo_class, algo_params = algorithms[algid]
            
            executions[key] = comp(run_combination, test_case, algo_class, algo_params,
                                   job_id='calib-%s-run' % exc_id)
    
            basename = join(options.outdir, 'results', '%s-%s' % (tcid, algid))
            comp(save_results, basename=basename,
                 results=executions[key],
                    job_id='calib-%s-save' % exc_id)        
            
            # Create iterations report
            report = comp(create_report_iterations, exc_id, executions[key],
                          job_id='calib-%s-report' % exc_id)
            
            filename = join(options.outdir, 'executions', '%s-%s.html' % (tcid, algid))
            comp(write_report, report, filename,
                 job_id='calib-%s-report-write' % exc_id)
            
        return executions[key]
     
    
    for comb_id in which:
        comb = combinations[comb_id]
        alg_ids = expand_string(comb.algorithms, algorithms.keys())
        tc_ids = expand_string(comb.test_cases, available_test_cases.keys())
        
        print('Set %r has %d test cases and %d algorithms (~%d jobs in total).' % 
          (comb_id, len(alg_ids), len(tc_ids), len(alg_ids) * len(tc_ids) * 2))

        deps = {}
        for t, a in itertools.product(tc_ids, alg_ids):
            deps[(t, a)] = stage_execution(t, a)

        job_id = 'tex-%s' % comb_id
        comp(create_tables_for_paper, comb_id, tc_ids, alg_ids, deps,
             job_id=job_id)
        
        job_id = 'set-%s-report' % comb_id
        report = comp(create_report_comb_stats,
                      comb_id, tc_ids, alg_ids, deps, job_id=job_id)
        
        job_id += '-write'
        filename = join(options.outdir, 'stats', '%s.html' % comb_id)
        comp(write_report, report, filename, job_id=job_id)

    if options.report or options.report_stats:
        if options.report:
            batch_command('clean *-report*')
        elif options.report_stats:
            batch_command('clean set-*  tex*')
        batch_command('parmake')
    elif options.remake:
        batch_command('clean *')
        batch_command('make set-* tex-*')
    else:
        compmake_console()

def test_case_generate(f, args):
    res = f(**args)
    assert isinstance(res, CalibTestCase)
    return res

def write_report(report, filename):
    print('Writing report %r to %r.' % (report.nid, filename))
    rd = join(os.path.dirname(filename), 'images')
    report.to_html(filename, resources_dir=rd)

def save_results(results, basename):
    
    # results = return values of run_combination
    filename = basename + '.mat'
    
    data = {}
    data['similarity'] = results['R'].astype('float32')
    data['S'] = results['S'].astype('float32')
    if 'true_S' in results:
        data['true_S'] = results['true_S'].astype('float32')
        data['S_aligned'] = align_distributions(data['S'], data['true_S'])
    else:
        print('no ground truth - no aligned points')
    data['description'] = """
   
   similarity:  input data
   true_S:  the ground truth given
   S: the estimated distribution
   s_aligned: the estimated distribution, aligned to true_S
    
"""
    data['creator'] = 'calib_main at %s' % isodate()
    import scipy.io
    make_sure_dir_exists(filename)
    print('Writing to %r.' % filename)
    scipy.io.savemat(filename, data, oned_as='row')
   

def isodate():
    """ E.g., '2011-10-06-22:54' """
    now = datetime.datetime.now()
    date = now.isoformat('-')[:16]
    return date

 
         
def run_combination(test_case, algo_class, algo_params):
    print('Running %s - %s(%s)' % (test_case.tcid, algo_class.__name__, algo_params))
    algo = algo_class(algo_params)
    if test_case.has_ground_truth:
        algo.solve(R=test_case.R, true_S=test_case.true_S)
    else:
        algo.solve(R=test_case.R)
        
    results = algo.results
    
    other = {#'test_case': test_case,
             'algo_class': algo_class,
             'combid': '%s-%s' % (test_case.tcid, algo) }
    
    results.update(other)
    return results

    
if __name__ == '__main__':
    main()
