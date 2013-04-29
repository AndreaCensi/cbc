from procgraph.core.block import Block
from cbc.algorithms.list_all import get_list_of_algorithms


class CBC(Block):
    Block.alias('cbc')
    
    Block.config('algo', default='CBC3dr50w')
    
    Block.input('R', 'Correlation')
    
    Block.output('cbc_results', 'Results dictionary')
    
    def init(self):
        algos = get_list_of_algorithms()
        algo = self.config.algo
        mine = algos[algo]
        ac, ap = mine
        self.cbc = ac(params=ap)

    def update(self):
        R = self.input.R
        self.info('solving') 
        results = self.cbc.solve(R, true_S=None)
        self.info('done')
        self.output.cbc_results = results

