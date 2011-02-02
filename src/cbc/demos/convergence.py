import itertools
import numpy as np
from cbc.tools import (best_embedding_on_sphere, distribution_radius,
                       scale_score, correlation_coefficient,
    cosines_from_directions, distances_from_directions, cosines_from_distances,
    random_directions_bounded, overlap_error_after_orthogonal_transform)
from reprep import Report

from contracts import disable_all
 
def simplified_algo(R, iterations, warp=0):
    S = best_embedding_on_sphere(R, ndim=3)
    R_order = scale_score(R).astype('int16')
    for i in range(iterations): #@UnusedVariable
        C = np.dot(S.T, S)
        C_sorted = np.sort(C.flat)
        R = C_sorted[R_order]
        S = best_embedding_on_sphere(R, ndim=3)
    
    if warp > 0:    
        base_D = distances_from_directions(S)
        diameter = base_D.max()
        min_ratio = 0.1
        max_ratio = np.pi / diameter
        ratios = np.exp(np.linspace(np.log(min_ratio), np.log(max_ratio), warp))
        scores = []
        guesses = []
        for ratio in ratios:
            Cwarp = cosines_from_distances(base_D * ratio)
            Sw = best_embedding_on_sphere(Cwarp, ndim=3)
            Cw_order = scale_score(cosines_from_directions(Sw))
            scores.append(correlation_coefficient(Cw_order, R_order))
            guesses.append(Sw)
        best = np.argmax(scores)
        print('Best warp: %d (%f)' % (best, ratios[best]))
        S = guesses[best]
    return S

def identity(x):
    return x    
    
def main():
    
    
    
    def spearman(a, b):
        ao = scale_score(a)
        bo = scale_score(b)
        return correlation_coefficient(ao, bo)
         
    disable_all()
    def seq():
        N = 180
        iterations = 10
        nradii = 100
        radii = np.linspace(5, 180, nradii)
        
        K = 1
        for radius_deg, i in itertools.product(radii, range(K)):
            print radius_deg, i
            # Generate a random symmetric matrix
            #x = np.random.rand(N, N)
            S = random_directions_bounded(3, np.radians(radius_deg), N)
            C = np.dot(S.T, S)
            alpha = 1
            f = lambda x: np.exp(-alpha * (1 - x))
            #f = lambda x : x
            R = f(C) 
            # Normalize in [0,1]
            R1 = (R - R.min()) / (R.max() - R.min())
            # Normalize in [-1,1]
            R2 = (R1 - 0.5) * 2
            
            S1 = simplified_algo(R1, iterations) 
            S1w = simplified_algo(R1, iterations, warp=50)
            S2 = simplified_algo(R2, iterations)

            s1 = spearman(cosines_from_directions(S1), R1)
            s1w = spearman(cosines_from_directions(S1w), R1)
            s2 = spearman(cosines_from_directions(S2), R2)
        
            e1 = np.degrees(overlap_error_after_orthogonal_transform(S, S1))
            e1w = np.degrees(overlap_error_after_orthogonal_transform(S, S1w))
            e2 = np.degrees(overlap_error_after_orthogonal_transform(S, S2))
            r0 = np.degrees(distribution_radius(S))
            r1 = np.degrees(distribution_radius(S1))
            r1w = np.degrees(distribution_radius(S1w))
            r2 = np.degrees(distribution_radius(S2))
            yield dict(R0=r0, R1=r1, R1w=r1w, R2=r2, e1=e1, e2=e2, s1=s1, s2=s2,
                       s1w=s1w, e1w=e1w)
    
    results = list(seq())
    data = dict((k, np.array([d[k] for d in results])) for k in results[0])
    
        
    r = Report('demo-convergence')
    
    api1 = 'pi1'
    api1w = 'pi1w'
    api2 = 'pi2'
    
    
    sets = [(data['R0'] < 90, 'r.'), (data['R0'] >= 90, 'g.')]
    
    f = r.figure('radius', cols=3, caption='radius of solution')
    with r.data_pylab('r0r1') as pylab:
        for sel, col in sets:
            x = data['R0'][sel]
            y = data['R1'][sel]
            pylab.plot(x, x, 'k--')
            pylab.plot(x, y, col)
             
        pylab.xlabel('real radius')
        pylab.ylabel('radius (pi1)')
        pylab.axis('equal')
    r.last().add_to(f, caption=api1)
    
    with r.data_pylab('r0r1w') as pylab:
        for sel, col in sets:
            x = data['R0'][sel]
            y = data['R1w'][sel]
            pylab.plot(x, x, 'k--')
            pylab.plot(x, y, col)
             
        pylab.xlabel('real radius')
        pylab.ylabel('radius (pi1 + warp)')
        pylab.axis('equal')
    r.last().add_to(f, caption=api1w)
    
    with r.data_pylab('r0r2') as pylab:
        for sel, col in sets:
            x = data['R0'][sel]
            y = data['R2'][sel]
            pylab.plot(x, x, 'k--')
            pylab.plot(x, y, col)
        pylab.xlabel('real radius')
        pylab.ylabel('radius (pi2)')
        pylab.axis('equal')
    r.last().add_to(f, caption=api2)
            
    with r.data_pylab('r1r2') as pylab:
        for sel, col in sets:
            pylab.plot(data['R1'][sel], data['R2'][sel], col) 

        pylab.xlabel('radius (pi1)')
        pylab.ylabel('radius (pi2)')
        pylab.axis('equal')
    r.last().add_to(f, 'Comparison %s - %s' % (api1, api2))
    
    with r.data_pylab('r1r1w') as pylab:
        for sel, col in sets:
            pylab.plot(data['R1'][sel], data['R1w'][sel], col) 

        pylab.xlabel('radius (pi1)')
        pylab.ylabel('radius (pi1+warp)')
        pylab.axis('equal')
    r.last().add_to(f, 'Comparison %s - %s' % (api1, api1w))
        
    f = r.figure('spearman', cols=3, caption='Spearman score')
    with r.data_pylab('r0s1') as pylab:
        for sel, col in sets:
            x = data['R0'][sel]
            y = data['s1'][sel]
            pylab.plot(x, y, col)
        pylab.xlabel('real radius')
        pylab.ylabel('spearman (pi1)')
    r.last().add_to(f, caption=api1)
    
    with r.data_pylab('r0s1w') as pylab:
        for sel, col in sets:
            x = data['R0'][sel]
            y = data['s1w'][sel]
            pylab.plot(x, y, col)
        pylab.xlabel('real radius')
        pylab.ylabel('spearman (pi1+warp)')
    r.last().add_to(f, caption=api1w)
        
    with r.data_pylab('r0s2') as pylab:
        for sel, col in sets:
            x = data['R0'][sel]
            y = data['s2'][sel]
            pylab.plot(x, y, col)
        pylab.xlabel('real radius')
        pylab.ylabel('spearman (pi2)')
    r.last().add_to(f, caption=api2)
        
    f = r.figure('final_error', cols=3, caption='Average absolute error')        
    with r.data_pylab('r0e') as pylab:
        x = data['R0']
        y = data['e1']
        pylab.plot(x, y, 'm-', label=api1)
        x = data['R0']
        y = data['e1w']
        pylab.plot(x, y, 'g-', label=api1w)
        x = data['R0']
        y = data['e2']
        pylab.plot(x, y, 'b-', label=api2)
        pylab.xlabel('real radius')
        pylab.ylabel('average error (deg)')
        pylab.legend()
    r.last().add_to(f)
        
        
    filename = 'cbc_demos/convergence.html'
    print("Writing to %r." % filename) 
    r.to_html(filename)
        
if __name__ == '__main__':
    main()
    


