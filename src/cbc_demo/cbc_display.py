from procgraph import Block
from procgraph_mpl.plot_generic import PlotGeneric
from procgraph_mpl.plot_anim import PlotAnim
from reprep.plot_utils.spines import turn_off_all_axes
import numpy as np
from cbc.tools.math_utils import distances_from_directions
from matplotlib.path import Path
from matplotlib import patches

def random_permutation(n, seed):
    ''' Returns a random permutation of n elements. '''
    # TODO: do not touch the global seed
    np.random.seed(seed)
    return np.argsort(np.random.rand(n))


class Shuffle2d(Block):
    Block.alias('shuffle2d')
    Block.input('y')
    Block.output('y2')
    
    def init(self):
        self.rp = None
        
    
    def update(self):
        y = self.input.y
        y2 = y.copy()
        if self.rp is None:
            n = y.shape[0] * y.shape[1]
            self.rp = random_permutation(n, seed=100)

        def shuffleit(x):
            return x[self.rp]
        
        for i in range(3):
            y2[..., i].flat = shuffleit(y[..., i].flatten())
    
        self.output.y2 = y2
    

class CBCDisplayDistLub(Block):
    Block.alias('cbc_display_dist_lum')

    Block.config('width', 'Image dimension', default=320)
    Block.config('height', 'Image dimension', default=320)
    
    Block.input('y0', 'image')
    Block.input('res', 'Results dictionary')
    
    Block.output('rgb')
    
    def init(self):
        self.plot_generic = PlotGeneric(width=self.config.width,
                                        height=self.config.height,
                                        transparent=False,
                                        tight=False,
                                        keep=True)
        self.plot_anim = PlotAnim()
        self.s = None
        
    def update(self):
        self.output.rgb = self.plot_generic.get_rgb(self.plot)
        
    def plot(self, pylab):
        res = self.input.res
        y0 = self.input.y0
        self.info(y0.shape)
        
        y0 = y0 / 255.0
        R = y0[..., 0].flatten()
        G = y0[..., 1].flatten()
        B = y0[..., 2].flatten()
        

        rgbs = zip(R, G, B)
#         rgbs = np.vstack((R, G, B)).T
#         print rgbs.shape
        
         
        
        if res is None or y0 is None: 
            return
        S = res['S']

        Sx = S[0, :]
        Sy = S[1, :]

#         _, N = S.shape 
#         assert rgbs.shape == (N, 3)

        fig = pylab.gcf()
        fig.patch.set_facecolor('black')

        if self.s is None:
            self.info('scatter')
            verts = [
                (-1., -1.),  # left, bottom
                (-1., 1.),  # left, top
                (1., 1.),  # right, top
                (1., -1.),  # right, bottom
                (-1., -1.),  # ignored
                ]

            codes = [Path.MOVETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.CLOSEPOLY,
                     ]
            
            path = Path(verts, codes)            
            patch = patches.PathPatch(path, facecolor='black', lw=0)
            pylab.gca().add_patch(patch)

            self.s = pylab.scatter(x=Sx, y=Sy, c=rgbs, zorder=1000)


        else:
            offs = np.array((Sx, Sy)).T
            self.s.set_offsets(offs)
            self.s.set_color(rgbs)
            
            
        pylab.axis((-1, +1, -1, +1))
        turn_off_all_axes(pylab)
    
    


class CBCDisplayDist(Block):
    Block.alias('cbc_display_dist')

    Block.config('width', 'Image dimension', default=320)
    Block.config('height', 'Image dimension', default=320)
    
    Block.input('res', 'Results dictionary')
    
    Block.output('rgb')
    
    def init(self):
        self.plot_generic = PlotGeneric(width=self.config.width,
                                        height=self.config.height,
                                        transparent=False,
                                        tight=False,
                                        keep=True)
        self.plot_anim = PlotAnim()
        
    def update(self):
        self.output.rgb = self.plot_generic.get_rgb(self.plot)
        
    def plot(self, pylab):
        res = self.input.res
        S = res['S']
        self.info(S.shape)
        
        Sx = S[0, :]
        Sy = S[1, :]
#         Sz = S[2, :]
        self.plot_anim.set_pylab(pylab)
        
        self.plot_anim.plot('Sxy', Sx, Sy, 'ko')
        pylab.axis((-1, +1, -1, +1))
        turn_off_all_axes(pylab)
    

class CBCDisplayRes(Block):
    Block.alias('cbc_display_f')

    Block.config('width', 'Image dimension', default=320)
    Block.config('height', 'Image dimension', default=320)
    
    Block.input('res', 'Results dictionary')
    
    Block.output('rgb')
    
    def init(self):
        self.plot_generic = PlotGeneric(width=self.config.width,
                                        height=self.config.height,
                                        transparent=False,
                                        tight=False,
                                        keep=False)
#         self.plot_anim = PlotAnim()
        
    def update(self):
        self.output.rgb = self.plot_generic.get_rgb(self.plot)
        
    def plot(self, pylab):
        
        
        res = self.input.res
        
        R = res['R']
        S = res['S']
        D = distances_from_directions(S)
        
        Rf = np.array(R.flat)
        Df = np.rad2deg(np.array(D.flat))
        
#         self.plot_anim.set_pylab(pylab)
#         self.plot_anim.plot('rel', Df, Rf, 'b.')
        pylab.plot(Df, Rf, 'b.')
        D1 = np.max(Df)
        pylab.axis((0, D1, -1, +1))
        pylab.xlabel('distance (deg)')
        pylab.ylabel('similarity')
#         turn_off_all_axes(pylab)
    
