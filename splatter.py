# splatter.py: Implements the blood splatter effect that gets spawned when ever a mob is hit, really knowing more then a simple animated sprite
# Author: Niklas Hedlund

from pygame import *
from animsprite import *

class Splatter(AnimSprite):
    def __init__(self, pos, splatterTextures):
        AnimSprite.__init__(self)
        self.pos = pos
        self.size = (32,32)

        self.textures = splatterTextures
        self.animKey = 40
        self.imageIndexes = [(0,0), [(0,0), (1,0), (2,0), (3,0)]]
        self.animEnable = True

    def isDead(self):
        return self.animHasRestarted
