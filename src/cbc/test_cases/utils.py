import numpy as np
import sys

def add_distance_noise(D, dist_noise):
    noise = np.random.randn(*(D.shape))
    D2 = D + dist_noise * D * noise
    return D2


class Ticker(object):
    def __init__(self, msg, num_expected=None, stream=sys.stderr):
        self.msg = msg
        self.num_expected = num_expected
        self.num = 0
        self.stream = stream
        self.current = None
        self.update()
        
    def update(self):
        s = '%s %4d %s' % (self.msg, self.num, self.current)
        self.stream.write(s.ljust(80))
        self.stream.write('\r')
        self.stream.flush()
            
    def __call__(self, value):
        self.current = value
        self.num += 1
        self.update()
        
