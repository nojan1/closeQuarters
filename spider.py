from mob import *

class Spider(Mob):
    def __init__(self, pos, ai, texture):
        Mob.__init__(self, ai, 3, 2)
        self.pos = pos
        self.size = (32,32)

        self.textures = texture
        self.animKey = 100
        self.imageIndexes = [(0,0), [(4,0), (5,0), (6,0), (7,0), (8,0), (9,0), (10,0), (11,0), (12,0)]]

    def draw(self, screen, game, numTicks = 0):
        self.hasActivated = False
        Mob.draw(self, screen, game, numTicks)
