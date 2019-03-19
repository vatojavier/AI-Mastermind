import itertools
import numpy as np

class AIEntity:
        guess = np.zeros((4,),dtype=int)
        info = np.zeros((4,),dtype=int)
        pool = np.zeros((625,),dtype=int) #[4,256] array
        allColors = 0
        nPegs = 0

        def __init__(self,allColors,nPegs):
            self.allColors  = allColors
            self.nPegs      = nPegs
            self.pool       = self.generate_pool() #generate the pool depending on number of colors

        #generates initial pool of 625 (with 5 different colors)
        def generate_pool(self):
            colors = []

            for i in range(self.allColors):
                colors.append(i + 1)

            pool_list   = [p for p in itertools.product(colors, repeat=4)]
            pool        = np.array(pool_list)
            return pool

        #makes a new guess
        def guess(self):

            guess = np.random.randint(1,high=self.allColors + 1, size=self.nPegs)
            return guess

        #reduces the pool
        def reduce_pool(self):
            #more hard part
            pass
