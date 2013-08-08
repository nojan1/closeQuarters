# animsprite.py: Base class for animated sprites, inherits sprite and works by loading the correct image into the 'active' image variable
# Author: Niklas Hedlund

from pygame import *
from textureset import *
from sprite import *

class AnimSprite(nSprite):
    def __init__(self):
        nSprite.__init__(self)

        self.textureOffset = (0,0)
        self.textures = None

        #The image indexes is the indexes that will be used for textureset methods, it is a list since this will vary depending on where in the animation we are
        self.imageIndexes = [(0,0),[]]

        #Enable animation
        self.animEnable = False
        #The current index in the list
        self.animIndex = 0
        #How often should the animation update
        self.animKey = 0
        #When was the animation laste updated
        self.animLast = 0

        self.animHasRestarted = False

    def nextImage(self):
        self.animIndex += 1
        if self.animIndex > len(self.imageIndexes) - 1:
            self.animIndex = 0
            self.animHasRestarted = True

        self.image = self.textures.getSeries(self.textureOffset, self.size, self.imageIndexes[1][self.animIndex])

    def draw(self, screen, game, numTicks):
        if self.animEnable:
            if numTicks - self.animLast > self.animKey:
                self.animLast = numTicks
                self.nextImage()
        else:
            self.image = self.textures.getSeries(self.textureOffset, self.size, self.imageIndexes[0])

        nSprite.draw(self, screen, game)
