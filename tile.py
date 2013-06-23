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
    def __init__(self, location):
        Tile.__init__(self, location)

    def draw(self, screen, game):
        screen.fill((100,100,100), self.getRectScreen(game))

class Wall(Tile):
    def __init__(self, location):
        Tile.__init__(self, location)

    def draw(self, screen, game):
        #print(self.getRect(), self.getRectScreen(game), game.getView())
        screen.fill((0,0,100), self.getRectScreen(game))
        
    def onCollision(self):
        return True
