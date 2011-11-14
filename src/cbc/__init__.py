__version__ = '1.0'

from contracts import contract, new_contract, check
import numpy as np
from compmake import comp, compmake_console, batch_command, use_filesystem

from reprep import Report

from nose.tools import nottest 
import cPickle as pickle

import logging
logger = logging.getLogger('calib')

