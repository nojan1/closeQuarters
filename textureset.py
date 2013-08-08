# textureset.py: Class the handle texture sets (also known as grid layouts), contains methods to extract single textures from this set. Also supports on the fly rotation 
# Author: Niklas Hedlund

from pygame import *
import os
import math

from config import *

class TextureSet(object):
    def __init__(self, imagename, colorkey=None):
        self.image = image.load(os.path.join(GRAPHICPATH, imagename))

        #If no custom colorkey was suplied we assume a alpha image
        if colorkey != None:
            self.image = self.image.convert()
            self.image.set_colorkey(colorkey)
        else:
            self.image = self.image.convert_alpha()

        #Cache all rotated images, to impromve performance
        self.rotationCache = {}

    #Get a texture from just offset (coordinates) and size
    def getSingle(self, offset, size):
        return self.image.subsurface(Rect(offset, size))

    #Get a texture from x,y coordinates (as well as offset which indicates the start of the grid and size of course)
    def getSeries(self, offset, size, coords):
        (x, y) = coords
        newOffset = (offset[0] + size[0] * x, offset[1] + size[1] * y)
        return self.getSingle(newOffset, size)
        
    #Same as getSingle but rotated
    def getSingleRotated(self, offset, size, angle):
        angle = math.degrees(angle)

        #Compute the search key which is used to in the cache
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
