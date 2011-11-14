from . import Report, contract, np
from ..tools import (best_embedding_on_sphere, distances_from_directions,
    correlation_coefficient, cosines_from_distances, cosines_from_directions,
    scale_score)
from optparse import OptionParser
import cPickle as pickle
import itertools

def main():
    
    parser = OptionParser()
    
    parser.add_option("--data",
            type="string", help='.pickle file containing data')

    (options, args) = parser.parse_args() #@UnusedVariable
    assert not args
    
    data = pickle.load(open(options.data, 'rb'))
    print data.keys()
    R = data['correlation']
    num_ref, num_sensels = R.shape 
    assert num_ref <= num_sensels
    imshape = (100, 100) # XXX
    toimg = lambda x: x.reshape(imshape)


    # find indices
    ref_sensel = np.zeros(num_ref, dtype='int')
    for i in range(num_ref):
        ref_sensel[i] = np.argmax(R[i, :])
        
    print ref_sensel
    # Which pixels where there?
    samples = np.zeros(num_sensels)
    samples[ref_sensel] = 1
    samples = toimg(samples)
    
    Rf = R[:, ref_sensel]
    
    R2 = np.empty_like(Rf)
    for i, j in itertools.product(range(num_ref), range(num_ref)):
        vi = R[i, :] 
        vj = R[j, :]
        norm = np.linalg.norm
        vi = vi / norm(vi)
        vj = vj / norm(vj)
        
        R2[i, j] = (vi * vj).sum()
    
    Sref_embed = reduced_rank_embed(R2, 3)
    #Sref_cbc = simplified_algo(R2, 3, iterations=8, warp=20)
     
    @contract(Sref='array[KxM]', ref_sensels='array[M]',
               similarity='array[MxN]', returns='array[KxN]')
    def interpolate(Sref, ref_sensels, similarity):
        num_sensels = similarity.shape[1]
        num_coords = Sref.shape[0] 
        S = np.zeros((num_coords, num_sensels))
        for i in range(num_coords):
            S[i, ref_sensels] = Sref[i, :]
            
        if True:
            for k in range(num_sensels):
                sim = similarity[:, k]
                # only interpolate between these
                keep = 10
                order = np.argsort(-sim)
                sim[order[keep + 1:]] = 0
                sim = sim / sim.sum()
                for i in range(num_coords):
                    S[i, k] = (Sref[i, :] * sim).sum() 
        return S
    
    Sref_embed_all = interpolate(Sref_embed, ref_sensel, R)
    
    r = Report()

    f = r.figure('data', cols=3)
    r.data('samples', samples).display('posneg').add_to(f)
    r.data('Rf', Rf).display('posneg').add_to(f)
    r.data('R2', R2).display('posneg').add_to(f)
    


    
    S = reduced_rank_embed(R, 4)
    
    r.add_child(show_some_correlations(R, toimg, num=30, cols=6)) 
    r.add_child(display_coordinates('embed', S, toimg))
    r.add_child(display_coordinates('ref+int', Sref_embed_all, toimg))
    
    colors = [(6, [1, 0, 0]),
              (1, [0, 1, 0]),
              (2, [0, 0, 1]),
              (13, [1, 0, 0]),
              (4, [0, 0, 1]),
              (5, [0, 1, 0]),
              ]
    Rrgb = colorful_correlation(R, toimg, colors)
    r.data_rgb('Rrgb', Rrgb).add_to(f)
    
    
    filename = 'cbc_demos/camera_plots.html'
    print("Writing to %r." % filename) 
    r.to_html(filename)

def colorful_correlation(R, toimg, colors):
    h, w = toimg(R[0, :]).shape
    rgb = np.zeros((h, w, 3), dtype='float32')
    for sensel, color in colors:
        r = R[sensel, :]
        best = np.argmax(r)
#        r[best] = 0
        r = np.maximum(0, r)
        r = r / r.max() 
        r[best] = 1
        
        im = toimg(r)
        for i in range(3):
            rgb[:, :, i] += im * 255 * (1 - color[i])
         
    rgb = 255 - rgb
    rgb = np.clip(rgb, 0, 255)
    
    return  rgb.astype('uint8')


@contract(S='array[MxN],M<N')
def display_coordinates(label, S, toimg):
    r = Report(label)
    M = S.shape[0]
    f = r.figure('Coordinates.', cols=M)
    
    for i in range(M):
        nid = 'coord%d' % i
        Si = toimg(S[i, :])
        r.data(nid, Si).display('posneg')
        f.sub(nid)
    return r    


@contract(R='array[KxN],K<=N', ndim='int,>0,M', returns='array[MxN]')
def reduced_rank_embed(R, ndim):
    K, N = R.shape #@UnusedVariable
    U, S, V = np.linalg.svd(R, full_matrices=0) #@UnusedVariable
    coords = V[:ndim, :]
    for i in range(ndim):
        coords[i, :] = coords[i, :] * np.sqrt(S[i])
    return coords

def show_some_correlations(R, toimg, num=30, cols=6):
    r = Report('sensels correlations')
    f = r.figure('Correlations of some sensels.', cols=cols)
    
    s = R.sum(axis=0)
    r.data('sum', toimg(s)).display('posneg')
    f.sub('sum', caption="Sum of correlations")
    
    for i in range(num):
        nid = 'sensel%d' % i
        Ri = toimg(R[i, :])
        r.data(nid, Ri).display('posneg')
        f.sub(nid)
    return r


def simplified_algo(R, ndim, iterations, warp=0):
    S = best_embedding_on_sphere(R, ndim)
    R_order = scale_score(R).astype('int16')
    for i in range(iterations): #@UnusedVariable
        C = np.dot(S.T, S)
        C_sorted = np.sort(C.flat)
        R = C_sorted[R_order]
        S = best_embedding_on_sphere(R, ndim)
    
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
            score = correlation_coefficient(Cw_order, R_order)
            scores.append(score)
            guesses.append(Sw)
            print('Ratio %5f score %.5f' % (ratio, score))
        best = np.argmax(scores)
        print('Best warp: %d (%f) score %.5f' % (best, ratios[best], scores[best]))
        S = guesses[best]
    return S

if __name__ == '__main__':
    main()
    

