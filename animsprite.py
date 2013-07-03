from pygame import *

from textureset import *
from sprite import *

class AnimSprite(nSprite):
    def __init__(self):
        nSprite.__init__(self)

        self.textureOffset = (0,0)
        self.textures = None
        self.imageIndexes = [(0,0),[]]

        self.animEnable = False

        self.animIndex = 0
        self.animKey = 0
        self.animLast = 0

    def nextImage(self):
        self.animIndex += 1
        if self.animIndex > len(self.imageIndexes) - 1:
            self.animIndex = 0

        self.image = self.textures.getSeries(self.textureOffset, self.size, self.imageIndexes[1][self.animIndex])

    def draw(self, screen, game, numTicks):
        if self.animEnabled:
            if numTicks - self.animLast > self.animKey:
                self.animLast = numTicks
                self.nextImage()
        else:
            self.image = self.textures.getSeries(self.textureOffset, self.size, self.imageIndexes[0])

        nSprite.draw(self, screen, game)
