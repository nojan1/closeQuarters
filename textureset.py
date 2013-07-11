from pygame import *
import os
import math

from config import *

class TextureSet(object):
    def __init__(self, imagename, colorkey=None):
        self.image = image.load(os.path.join(GRAPHICPATH, imagename))

        if colorkey != None:
            self.image = self.image.convert()
            self.image.set_colorkey(colorkey)
        else:
            self.image = self.image.convert_alpha()

        self.rotationCache = {}

    def getSingle(self, offset, size):
        return self.image.subsurface(Rect(offset, size))

    def getSeries(self, offset, size, coords):
        (x, y) = coords
        newOffset = (offset[0] + size[0] * x, offset[1] + size[1] * y)
        return self.getSingle(newOffset, size)
        
    def getSingleRotated(self, offset, size, angle):
        angle = math.degrees(angle)
        searchKey = str(offset) + str(size) + str(angle)

        if searchKey in self.rotationCache:
            return self.rotationCache[searchKey]
        else:
            image = self.getSingle(offset, size)
            image = transform.rotate(image, angle)
            self.rotationCache[searchKey] = image
            return image

    def getSeriesRotated(self, offset, size, coords, angle):
        (x, y) = coords
        newOffset = (offset[0] + size[0] * x, offset[1] + size[1] * y)
        return self.getSingleRotated(newOffset, size, angle)
