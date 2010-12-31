from snp_geometry.random_geometry import \
    random_direction, geodesic_distance_on_S2, \
    rotation_from_axis_angle
from cbc.tools.math_utils import distances_from_directions, \
     cosines_from_distances, directions_from_angles
import numpy as np
from contracts import contracts
from reprep import Report

@contracts(N='int,>0,N',
           radius_deg='number,>0,<=180',
           returns='array[3xN], directions')
def get_distribution(ndim, N, radius_deg):
    radius = np.radians(radius_deg)
    
    if ndim == 3:
        center = random_direction()
        @contracts(returns='direction')
        def one():
            axis = random_direction()
            angle = np.random.rand() * radius
            R = rotation_from_axis_angle(axis, angle)
            v = np.dot(R, center)
            
            dist = geodesic_distance_on_S2(center, v)
            assert dist <= angle # equal only if perpendicular axis
            assert dist <= radius
            return v
            
        return np.vstack([one() for i in range(N)]).T #@UnusedVariable
    elif ndim == 2:
        center = np.random.rand() * 2 * np.pi
        diffs = (np.random.rand(N) - 0.5) * 2 * radius
        angles = diffs + center
        return directions_from_angles(angles)
    else:
        assert False, 'Only ndim=2,3 supported.'
    
        
def svds(M, n):
    U, sv, V = np.linalg.svd(M, full_matrices=0) #@UnusedVariable
    return sv[:n]
    
    
def main():
    N = 100
    radius_deg = 50
    num_svds = 8
    warps = sorted(list(np.linspace(0.5, 1.5, 5)) + [0.9, 0.95, 1.05, 1.1]) 

    r = Report('warp analysis')
    warps_desc = ", ".join(['%.2f' % x for x in warps])
    caption = """ This figure shows that on S^1 things can be warped easily.
    The initial distribution of {N} points, with radius {radius_deg},
    is warped with warps equal to {warps_desc}. In 2D the rank is still 2, while
    in 3D the warped distances cannot be embedded on the sphere. 
    The reason is that S^1 is a manifold with curvature 0, while S^2 has
    curvature 2*pi. 
    """.format(**locals()) 
    
    f = r.figure(caption=caption)

    for ndim in [2, 3]:
        S = get_distribution(ndim, N, radius_deg)
        D = distances_from_directions(S)
        assert np.degrees(D.max()) <= 2 * radius_deg
        
        with r.data_pylab('svds%d' % ndim) as pylab:    
            for warp in warps:
                Dw = D * warp
                Cw = cosines_from_distances(Dw)
                s = svds(Cw, num_svds)
                pylab.semilogy(s, 'x-', label='%.2f' % warp)
            pylab.legend()
        r.last().add_to(f,
            caption='Singular value for warped distances (ndim=%d)' % ndim)
    
    filename = 'cbc_demos/warp.html'
    print("Writing to %r." % filename) 
    r.to_html(filename)

if __name__ == '__main__':
    main()
    


