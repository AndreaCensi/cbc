import numpy as np
from .math_utils import get_angles_from_S, create_s_from_theta
from snp_geometry.utils import assert_allclose

def get_angles_from_S_test():
    theta = np.random.rand(120) * np.pi * 2 - np.pi 
    S = create_s_from_theta(theta)
    theta2 = get_angles_from_S(S)
    assert_allclose(theta, theta2)

