from . import load_test_case
import os

def standard_test_dir(dirname):
    tcs = {}
    for d in os.listdir(dirname):        
        tcdir = os.path.join(dirname, d) 
        tcs[d] = (load_test_case, dict(dirname=tcdir))
    return tcs
    
