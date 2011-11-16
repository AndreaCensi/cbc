from . import CalibTestCase, contract, check, np, nottest, pickle
from ..tools import cov2corr, directions_from_angles, scale_score
from ..utils import Ticker
import itertools
import sys

@nottest
@contract(returns='dict(str: tuple(Callable, dict))')
def get_real_test_cases(filename):
    print('Loading Sick data from disk...')
    with open(filename) as f: 
        data = pickle.load(f)
    print('...done.')

    # Try separately and together
    selections = [ ('sick_front', np.array(range(181))),
                   ('sick_rear', np.array(range(181, 362))),
                   ('sick_both', np.array(range(362))) ]
    check('list(tuple(str, $(array[M], M>0, M<=362) ))', selections)
    ground_truth = np.linspace(0, np.pi * 2, 362)
    
    # Compute information distance
    print('Computing information distance from joint statistics...')
    h, hdist = compute_hdist(data['single'], data['joint']) #@UnusedVariable
    infsim = np.cos(hdist * np.pi)

    print('Computing correlations from covariances...')
    statistics = [ ('y_corr', cov2corr(data['y_cov'])),
                  ('y_dot_corr', cov2corr(data['y_dot_cov'])),
                  ('y_dot_sign_corr', cov2corr(data['y_dot_sign_cov'])),
                  ('y_dot_abs_corr', cov2corr(data['y_dot_abs_cov'])),
                   ('y_infsim', infsim)]
    
    check('list(tuple(str, array[362x362]))', statistics)
    
    tcs = {}
    ticker = Ticker('Generating real cases')
    def add_test_case(tcid, function, args):
        ticker(tcid)
        tcs[tcid] = (function, args)

    # The basic statistics
    for sel, stat in itertools.product(selections, statistics):
        selid, select = sel
        statid, bigR = stat
        
        R = bigR[select, :][:, select]
        
        angles = ground_truth[select]
        S = directions_from_angles(angles)
        
        tcid = '%s-%s' % (selid, statid)
        add_test_case(tcid, test_case, dict(tcid=tcid, R=R, S=S, kernel=None))

    # The combined statistics
    for sel in selections:        
        selid, select = sel
        S = directions_from_angles(ground_truth[select])
        
        # Put all of these together
        vars = ['y_corr', 'y_dot_sign_corr', 'y_dot_abs_corr', 'y_dot_corr', 'y_infsim'] #@ReservedAssignment
        all = dict(statistics) #@ReservedAssignment
        raws = [all[k] for k in vars]
        scores = [scale_score(x[select, :][:, select]) for x in raws]
        RR = scores[0] + scores[1] + scores[2] + scores[4]
        
        Rmax = np.max(scores, axis=0)
        
        assert Rmax.shape == RR.shape        
        
        tcid = '%s-%s' % (selid, 'mix')
        add_test_case(tcid, test_case, dict(tcid=tcid, R=RR, S=S, kernel=None))
        
        tcid = '%s-%s' % (selid, 'max')
        add_test_case(tcid, test_case, dict(tcid=tcid, R=Rmax, S=S, kernel=None))

    return tcs

@nottest
def test_case(tcid, R, S, kernel):
    tc = CalibTestCase(tcid, R)
    tc.set_ground_truth(S, kernel=kernel)
    return tc

@contract(single='array[NxK]', joint='array[NxNxKxK]',
           returns='tuple(array[N],array[NxN])')
def compute_hdist(single, joint):
    N, _ = single.shape
    
    H = np.zeros(N)
    for i in range(N):
        H[i] = shannon_entropy(single[i, :])
    
    Hi = np.tile(H, (N, 1))
    Hj = np.tile(H.reshape(N, 1), (1, N))
    
    R = np.zeros((N, N))    
    for i, j in itertools.product(range(N), range(N)):
        R[i, j] = shannon_entropy(joint[i, j, :, :])
    
    D = (2 * R - Hi - Hj) / R
    
    D = np.clip(D, 0, 1)

    return H, D

#@contract(f='array(>=0)', returns='float,>=0')
def shannon_entropy(f):
    s = f.sum()
    if s == 0:
        raise Exception('Empty distribution')
    pd = f.flatten().astype('float64') / s
    zeros, = np.nonzero(pd == 0)
    pd[zeros] = 1
    logpd = np.log(pd)
    pd[zeros] = 0

    return -(pd * logpd).sum()
    

if __name__ == '__main__':
    filename = sys.argv[1]
    data = pickle.load(open(filename, 'rb'))
    h, hdist = compute_hdist(data['single'], data['joint'])

    pickle.dump(hdist, open('hdist.pickle', 'wb'))

    hdist = np.cos(hdist * np.pi)
    e = -np.eye(hdist.shape[0]) + 1
    hdist = hdist * e
        
    from reprep import Report
    r = Report()
    f = r.figure()
    r.data('hdist', hdist).display('scale').add_to(f)
    with r.data_pylab('h')as pylab:
        pylab.plot(h)
    r.last().add_to(f)
    filename = 'real_test_cases.html'
    print('Writing to %r.' % filename)
    r.to_html(filename)

    
    
