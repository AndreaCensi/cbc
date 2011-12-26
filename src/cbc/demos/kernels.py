from ..tc.synthetic import linear01_sat, pow3_sat, pow7_sat
from ..tools import distances_from_directions, cosines_from_directions
from reprep import Report
from warp import svds, get_distribution
import numpy as np


def identity(x):
    return x


def main():
    N = 100
    num_svds = 8

    radius_deg = 180

    kernels = [identity, linear01_sat, pow3_sat, pow7_sat]
#    kernels = [linear01_sat, pow3_sat, pow7_sat]

    r = Report('eig analysis')
#    warps_desc = ", ".join(['%.2f' % x for x in warps])
    caption = """ This figure shows that on S^1 things can be warped easily.
    The initial distribution of {N} points, with radius {radius_deg}.
    """.format(**locals())

    f = r.figure(caption=caption)
    mime = 'application/pdf'
    figsize = (4, 3)
    with r.data_pylab('kernels', mime=mime, figsize=figsize) as pylab:

        for kernel in kernels:
            x = np.linspace(-1, +1, 256)
            y = kernel(x)
            pylab.plot(x, y, label=kernel.__name__)
        pylab.axis([-1, 1, -1, 1])
        pylab.xlabel('Cosine between orientations')
        pylab.ylabel('Correlation')
        pylab.legend(loc='lower right')

    r.last().add_to(f, caption='Correlation kernels')

    for ndim in [2, 3]:
        S = get_distribution(ndim, N, radius_deg)
        C = cosines_from_directions(S)
        D = distances_from_directions(S)
        assert np.degrees(D.max()) <= 2 * radius_deg

        with r.data_pylab('svds%d' % ndim,
                          mime=mime, figsize=figsize) as pylab:
            for kernel in kernels:
                Cw = kernel(C)
                # TODO: 
                # Cw = cos(kernel(D))
                s = svds(Cw, num_svds)
                pylab.semilogy(s, 'x-', label=kernel.__name__)
            pylab.legend(loc='center right')
        r.last().add_to(f,
            caption='Singular value for different kernels (ndim=%d)' % ndim)

    filename = 'cbc_demos/kernels.html'
    print("Writing to %r." % filename)
    r.to_html(filename)

if __name__ == '__main__':
    main()



