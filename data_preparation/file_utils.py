import os


def should_exist(filename):
    if not os.path.exists(filename):
        raise Exception('I expected the file %r to exist.' % filename)
