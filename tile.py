# tile.py: Contains the different tiles that makes up the game world, handles all the logic for drawing as well as the events that happens when they are stepped on
# Author: Niklas Hedlund 

from pygame import *
from config import *
from sprite import *

import random

class Tile(nSprite):
    def __init__(self, location, image = None):
        nSprite.__init__(self)
        
        self.image = image
        self.pos = (location[0] * TILESIZE[0], location[1] * TILESIZE[1])
        self.size = TILESIZE

class Floor(Tile):
    def __init__(self, location, tileTextures):
        Tile.__init__(self, location, tileTextures.getSeries((0,0),TILESIZE, (random.randint(29, 33), 13)))

class Empty(Tile):
    def __init__(self, location, tileTextures):
        Tile.__init__(self, location)

    def draw(self, screen, game, numTicks = 0):
        pass
        
    def onCollision(self, game, isPlayer):
        return True

class Wall(Tile):
    def __init__(self, location, tileTextures):
        Tile.__init__(self, location, tileTextures.getSeries((0,0),TILESIZE, (random.randint(8, 15), 16)))
        
    def onCollision(self, game, isPlayer):
        return True

class MapChange(Floor):
    def __init__(self, location, tileTextures, newMapID):
        Floor.__init__(self, location, tileTextures)
        self.mapID = newMapID

    def onCollision(self, game, isPlayer):
        if isPlayer:
            game.changeMap(self.mapID)

        return True
