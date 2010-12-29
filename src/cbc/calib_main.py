import os
import itertools
import cPickle as pickle
from collections import namedtuple
from optparse import OptionParser, OptionGroup
from compmake import comp, compmake_console, batch_command

from contracts import check

from .algorithms import get_list_of_algorithms
from .test_cases import (get_syntethic_test_cases, get_real_test_cases)
from .reports import (create_report_test_case, create_report_comb_stats,
                      create_report_iterations)
from .tools import expand_string 

from compmake import use_filesystem
import numpy


join = os.path.join

def main():
    parser = OptionParser()

    group = OptionGroup(parser, "Files and directories")

    group.add_option("--outdir",
                      help='Directory with variables.pickle and where '
                           'the output will be placed.')

    group.add_option("--data", help='.pickle file containing data.')
    
    parser.add_option_group(group)

    group = OptionGroup(parser, "Experiments options")
    
    group.add_option("--set", default='*',
                      help='[= %default] Which combinations to run.')

    group.add_option("--seed", default=42, type='int',
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
    
    print('Available %d test cases and %d algorithms' % 
          (len(test_cases), len(algorithms)))
#    print('Available algos: %s.' % ", ".join(natsorted(algorithms.keys())))
#    print('Available testcases: %s.' % ", ".join(natsorted(test_cases.keys())))
    
    print('Random1: %f' % numpy.random.rand())
    print('Random2: %f' % numpy.random.randn())
    
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
     
    print('Creating list of combinations..')
    combinations = {}
    Combination = namedtuple('Combination', 'algorithms test_cases')
    combinations['all'] = Combination('*', '*')
    combinations['CBC'] = Combination(['cbc'], '*')
    combinations['CBC_vs_embed2'] = Combination(['cbc', 'embed2'], '*')
    combinations['CBCt'] = Combination('cbct*', '*')
#    combinations['tmp'] = Combination('cbct*', ['fov180-pow7*', 'fov360-pow7*'])
    combinations['tmp'] = Combination(['embed2', 'cbc'], ['fov135-identity'])
    combinations['tmp2'] = Combination(['cheat', #'rand',
                                        'embed2', 'cbc', 'cbct2'],
                                       ['fov135-linear01',
                                        'fov135-pow3_sat',
                                        'fov360-pow3_sat'])

    combinations['pow3'] = Combination(['cheat', #'rand',
                                        'embed2', 'cbc', 'cbct2'],
                                       ['fov135-pow3_sat',
                                        'fov180-pow3_sat',
                                        'fov225-pow3_sat',
                                        'fov360-pow3_sat'])
    
    combinations['tmp3'] = Combination(['cbc1pi', 'cbc2pi', 'embed2', 'cheat'],
                                       ['fov45-pow3_sat',
                                        'fov90-pow3_sat',
                                        'fov135-linear01',
                                        'fov270-linear01',
                                        'fov135-pow3_sat',
                                        'fov180-pow3_sat',
                                        'fov225-pow3_sat',
                                        'fov270-pow3_sat',
                                        'fov360-pow3_sat'])
    
    combinations['tmp4'] = Combination(['cbc2pia', 'embed2', 'cheat'],
                        ['fov135-pow3_sat', 'fov225-pow3_sat', 'fov270-pow3_sat'])

    combinations['real'] = Combination(['rand', 'cheat', 'cbc', 'cbc_t50'],
                                            'sick_*')
    
    which = expand_string(options.set, list(combinations.keys()))
    print('I will use the sets: %s' % which)
    if len(which) == 1:    
        compmake_storage = join(options.outdir, 'compmake', which[0])
    else:
        compmake_storage = join(options.outdir, 'compmake', 'common_storage')
    
    use_filesystem(compmake_storage)

    for comb_id in which:
        comb = combinations[comb_id]
        alg_ids = expand_string(comb.algorithms, algorithms.keys())
        tc_ids = expand_string(comb.test_cases, test_cases.keys())
        
        print('Set %r has %d test cases and %d algorithms (~%d jobs in total).' % 
          (comb_id, len(alg_ids), len(tc_ids), len(alg_ids) * len(tc_ids) * 2))

        deps = {}
        for t, a in itertools.product(tc_ids, alg_ids):
            deps[(t, a)] = stage_execution(t, a)
    
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
            batch_command('clean set-*-report*')
        batch_command('parmake')
    elif options.remake:
        batch_command('clean *')
        batch_command('make')
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
