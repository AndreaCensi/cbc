import os
import itertools
import cPickle as pickle
from collections import namedtuple
from optparse import OptionParser
from compmake import comp, compmake_console

from contracts import check

from .algorithms import get_list_of_algorithms
from .test_cases import (get_syntethic_test_cases, get_real_test_cases)
from .reports import (create_report_test_case, create_report_comb_stats,
                      create_report_iterations)
from .tools import expand_string


join = os.path.join

def main():
    
    parser = OptionParser()

    parser.add_option("--data", help='.pickle file containing data.')

    parser.add_option("--set", default='*',
                      help='Which combinations to run.')

    parser.add_option("--outdir", help='Directory with variables.pickle and where '
                                    'the output will be placed.')

    (options, args) = parser.parse_args() #@UnusedVariable
    assert not args
    assert options.data is not None 
    assert options.outdir is not None 
    
    print('Generating syntethic test cases...')
    synthetic = get_syntethic_test_cases()
    
    print('Reading real data...')
    data = pickle.load(open(options.data, 'rb'))
    real = get_real_test_cases(data)
    test_cases = {}
    test_cases.update(synthetic)
    test_cases.update(real)
    check('dict(str: test_case)', test_cases)

    print('Creating list of algorithms..')
    algorithms = get_list_of_algorithms()    
    check('dict(str: tuple(Callable, dict))', algorithms)

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
            
            # Create iterations report
            job_id = 'calib-%s-%s-report' % (tcid, algid)
            report = comp(create_report_iterations, results, job_id=job_id)
            
            job_id += '-write'
            filename = join(options.outdir, 'executions', '%s.html' % comb_id)
            comp(write_report, report, filename, job_id=job_id)
            
        return executions[key]
     
    print('Creating list of combinations..')
    combinations = {}
    Combination = namedtuple('Combination', 'algorithms test_cases')
    combinations['all'] = Combination('*', '*')
    combinations['CBC'] = Combination(['cbc'], '*')
    combinations['CBCt'] = Combination('cbct*', '*')
    combinations['tmp'] = Combination('cbc*', ['fov180-pow7*', 'fov360-pow7*'])

    which = expand_string(options.set, list(combinations.keys()))
    
    for comb_id in which:
        comb = combinations[comb_id]
        alg_ids = expand_string(comb.algorithms, algorithms.keys())
        tc_ids = expand_string(comb.test_cases, test_cases.keys())
        
        deps = {}
        for t, a in itertools.product(tc_ids, alg_ids):
            deps[(t, a)] = stage_execution(t, a)
    
        job_id = 'set-%s-report' % comb_id
        report = comp(create_report_comb_stats,
                      comb_id, tc_ids, alg_ids, deps, job_id=job_id)
        
        job_id += '-write'
        filename = join(options.outdir, 'stats', '%s.html' % comb_id)
        comp(write_report, report, filename, job_id=job_id)

    compmake_console()



def write_report(report, filename):
    print('Writing to %r.' % filename)
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
