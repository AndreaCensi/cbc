import os
import itertools
from optparse import OptionParser, OptionGroup
from compmake import comp, compmake_console, batch_command, use_filesystem

import numpy

from contracts import check
from contracts.enabling import disable_all

from .algorithms import get_list_of_algorithms
from .test_cases import (get_syntethic_test_cases, get_real_test_cases)
from .reports import (create_report_test_case, create_report_comb_stats,
                      create_report_iterations)
from .tools import expand_string 

from cbc.test_cases.fly import get_fly_testcase 
from cbc.combinations import get_list_of_combinations
from cbc.reports.paper_tables import create_tables_for_paper

join = os.path.join
# cbc_main --data_sick cbc_submission_data/sick.pickle \                                            
#          --data_fly  cbc_submission_data/fly.pickle \
#          --set 'paper*' --fast \
#          --outdir cbc_main_output
             
def main():
    parser = OptionParser()

    group = OptionGroup(parser, "Files and directories")

    group.add_option("--outdir",
                      help='Directory with variables.pickle and where '
                           'the output will be placed.')

    group.add_option("--data_sick", default=None,
                     help='.pickle file containing Sick data.')
    group.add_option("--data_fly", default=None,
                     help='.pickle file containing fly simulation data.')
    
    parser.add_option_group(group)

    group = OptionGroup(parser, "Experiments options")

    group.add_option("--fast", default=False, action='store_true',
                      help='Disables sanity checks.')
    
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
    
    
    numpy.random.seed(options.seed)    
    
    if options.fast:
        disable_all()

    assert not args 
    assert options.outdir is not None 
    
    test_cases = {}
    
    print('Generating synthetic test cases...')
    synthetic = get_syntethic_test_cases()
    test_cases.update(synthetic)
    
    if options.data_sick is not None:
        print('Preparing Sick data...')
        real = get_real_test_cases(options.data_sick)
        test_cases.update(real)
    
    if options.data_fly is not None:
        print('Preparing fly data...')
        test_cases.update(get_fly_testcase(options.data_fly))
        
    check('dict(str: tuple(Callable, dict))', test_cases)


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

    # Stage creation of test cases
    for k in list(test_cases.keys()):
        command, args = test_cases[k]
        job_id = 'test_case_data-%s' % k
        test_cases[k] = comp(command, job_id=job_id, **args)

    
    print('Available %d test cases and %d algorithms' % 
          (len(test_cases), len(algorithms)))
    
    print('Staging creation of test cases reports')
    test_case_reports = {} 
    def stage_test_case_report(tcid):
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
        stage_test_case_report(tcid)
        
        key = (tcid, algid)
        if not key in executions:
            test_case = test_cases[tcid]
            algo_class, algo_params = algorithms[algid]
            job_id = 'calib-%s-%s-run' % (tcid, algid)
            results = comp(run_combination, test_case, algo_class, algo_params,
                            job_id=job_id)
            executions[key] = results
            
            exc_id = '%s-%s' % (tcid, algid)
            # Create iterations report
            job_id = 'calib-%s-report' % exc_id
            report = comp(create_report_iterations, exc_id, results, job_id=job_id)
            
            job_id += '-write'
            filename = join(options.outdir, 'executions', '%s-%s.html' % (tcid, algid))
            comp(write_report, report, filename, job_id=job_id)
            
        return executions[key]
     
    
    for comb_id in which:
        comb = combinations[comb_id]
        alg_ids = expand_string(comb.algorithms, algorithms.keys())
        tc_ids = expand_string(comb.test_cases, test_cases.keys())
        
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



def write_report(report, filename):
    print('Writing report %r to %r.' % (report.id, filename))
    rd = join(os.path.dirname(filename), 'images')
    report.to_html(filename, resources_dir=rd)


def run_combination(test_case, algo_class, algo_params):
    print('Running %s - %s(%s)' % (test_case.tcid, algo_class.__name__, algo_params))
    algo = algo_class(algo_params)
    if test_case.has_ground_truth:
        algo.solve(R=test_case.R, true_S=test_case.true_S)
    else:
        algo.solve(R=test_case.R)
        
    results = algo.results
    
    other = {'test_case': test_case,
             'algo_class': algo_class,
             'combid': '%s-%s' % (test_case.tcid, algo) }
    
    results.update(other)
    return results

    
if __name__ == '__main__':
    main()
