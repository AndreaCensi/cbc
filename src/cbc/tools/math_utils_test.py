import numpy as np
from .math_utils import angles_from_directions, directions_from_angles
from snp_geometry.utils import assert_allclose

def get_angles_from_S_test():
    theta = np.random.rand(120) * np.pi * 2 - np.pi 
    S = directions_from_angles(theta)
    theta2 = angles_from_directions(S)
    assert_allclose(theta, theta2)

