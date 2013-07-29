# spider.py: Holds the Spider class which is one of the mobs in the game
# inherits Mob and just sets up the different attributes (textures and such)
# Author: Niklas Hedlund

from mob import *

class Spider(Mob):
    def __init__(self, pos, ai, texture):
        Mob.__init__(self, ai, 1, 1, 4)
        self.pos = pos
        self.size = (32,32)

        self.textures = texture
        self.animKey = 100
        self.imageIndexesTable = [[(0,5), [(4,5), (5,5), (6,5), (7,5), (8,5), (9,5), (10,5), (11,5), (12,5)]],
                                  [(0,6), [(4,6), (5,6), (6,6), (7,6), (8,6), (9,6), (10,6), (11,6), (12,6)]],
                                  [(0,7), [(4,7), (5,7), (6,7), (7,7), (8,7), (9,7), (10,7), (11,7), (12,7)]],
                                  [(0,0), [(4,0), (5,0), (6,0), (7,0), (8,0), (9,0), (10,0), (11,0), (12,0)]],
                                  [(0,1), [(4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1)]],
                                  [(0,2), [(4,2), (5,2), (6,2), (7,2), (8,2), (9,2), (10,2), (11,2), (12,2)]],
                                  [(0,3), [(4,3), (5,3), (6,3), (7,3), (8,3), (9,3), (10,3), (11,3), (12,3)]],
                                  [(0,4), [(4,4), (5,4), (6,4), (7,4), (8,4), (9,4), (10,4), (11,4), (12,4)]]]
