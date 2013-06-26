from pygame import *
import os

from config import *

class TextureSet(object):
    def __init__(self, imagename, colorkey=None):
        self.image = image.load(os.path.join(GRAPHICPATH, imagename)).convert()

        if colorkey != None:
            self.image.set_colorkey(colorkey)

    def getSingle(self, offset, size):
        return self.image.subsurface(Rect(offset, size))

    def getSeries(self, offset, size, coords):
        (x, y) = coords
        newOffset = (offset[0] + size[0] * x, offset[1] + size[1] * y)
        return self.getSingle(newOffset, size)
