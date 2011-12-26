from . import CalibTestCase, SPHERICAL
import cPickle as pickle
import os


def tc_load_spec(spec):
    name, _ = spec['format']

    if name == 'calib_pickle':
        return tc_load_spec_format10(spec)

    raise Exception('Unknown format %r.' % spec['format'])


def tc_load_spec_format10(spec):
    name, version = spec['format']
    assert name == 'calib_pickle'
    assert version[0] == 1
    assert version[1] >= 0

    file_should_exist(spec['data'])
    data = pickle.load(open(spec['data'], 'rb'))
    R = data['similarity']

    attrs = spec['attrs']

    # added in 1.1
    geometry = spec.get('geometry', SPHERICAL)

    tc = CalibTestCase(spec['id'], R,
                       geometry=geometry,
                       attrs=attrs)

    if 'gt' in spec:
        file_should_exist(spec['gt'])
        gt = pickle.load(open(spec['gt'], 'rb'))
        S = gt['true_S']
        tc.set_ground_truth(S, kernel=None)

    return tc


def file_should_exist(filename):
    if not os.path.exists(filename):
        raise Exception('File %r does not exist.' % filename)

