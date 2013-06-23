from config import *
from sprite import *

class Player(nSprite):
    def __init__(self, pos):
        nSprite.__init__(self)
        self.pos = pos
        self.size = (10,10)

        self.facingAngle = 0

    def move(self, xMove, yMove, worldMap):
        tmpRect = self.getRect()
        
        xMove *= PLAYERMOVE
        yMove *= PLAYERMOVE
        tmpRect.move_ip(xMove, yMove)

        if worldMap.isAllowedPosition(tmpRect):
            self.pos = tmpRect.topleft

    def draw(self, screen, game):
        screen.fill((255,0,0), self.getRectScreen(game))

        
