from . import np

def add_distance_noise(D, dist_noise):
    noise = np.random.randn(*(D.shape))
    D2 = D + dist_noise * D * noise
    return D2

