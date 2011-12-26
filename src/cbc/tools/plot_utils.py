from . import np


def create_histogram_2d(x, y, resolution):
    edges = np.linspace(-1, 1, resolution)
    H, _, _ = np.histogram2d(x.flatten(), y.flatten(), bins=(edges, edges))
    return H

