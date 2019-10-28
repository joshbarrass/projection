import numpy as np

class Cube(object):
    def __init__(self, length):
        self.a = length
        a = length

        self.vert = np.array(
            [[0,0,0], [a,0,0],
             [0,a,0], [a,a,0],
             [0,0,a], [a,0,a],
             [0,a,a], [a,a,a]]
            )

        self.edge = [
            (0,1), (0,2),
            (1,3), (2,3),
            (0,4), (1,5),
            (2,6), (3,7),
            (4,5), (4,6),
            (5,7), (6,7)]
        
