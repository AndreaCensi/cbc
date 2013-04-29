from procgraph import Block
from procgraph_mpl.plot_generic import PlotGeneric
from procgraph_mpl.plot_anim import PlotAnim
from reprep.plot_utils.spines import turn_off_all_axes
import numpy as np
from cbc.tools.math_utils import distances_from_directions

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
    
