# zombie.py: Holds the Zombie class which is one of the mobs in the game
# inherits Mob and just sets up the different attributes (textures and such)
# Author: Niklas Hedlund

from mob import *

class Zombie(Mob):
    def __init__(self, pos, ai, zombieTextures):
        Mob.__init__(self, ai, 2, 1)
        self.pos = pos
        self.size = (32,32)

        self.textures = zombieTextures
        self.animKey = 100
        self.imageIndexes = [(0,0), [(4,0), (5,0), (6,0), (7,0), (8,0), (9,0), (10,0), (11,0)]]

    def draw(self, screen, game, numTicks = 0):
        self.hasActivated = False
        Mob.draw(self, screen, game, numTicks)
