from pygame import *
from config import *
from sprite import *

class Tile(nSprite):
    def __init__(self, location, image = None):
        nSprite.__init__(self)
        
        self.image = image
        self.pos = (location[0] * TILESIZE[0], location[1] * TILESIZE[1])
        self.size = TILESIZE

class Floor(Tile):
    def __init__(self, location, tileTextures):
        Tile.__init__(self, location, tileTextures.getSeries((0,0),TILESIZE, (0,1)))

class Empty(Tile):
    def __init__(self, location, tileTextures):
        Tile.__init__(self, location)

    def draw(self, screen, game, numTicks = 0):
        pass
        
    def onCollision(self, game):
        return True

class Wall(Tile):
    def __init__(self, location, tileTextures):
        Tile.__init__(self, location, tileTextures.getSeries((0,0),TILESIZE, (1,1)))
        
    def onCollision(self, game):
        return True

class MapChange(Floor):
    def __init__(self, location, tileTextures, newMapID):
        Floor.__init__(self, location, tileTextures)
        self.mapID = newMapID

    def onCollision(self, game):
        game.changeMap(self.mapID)
        return True
