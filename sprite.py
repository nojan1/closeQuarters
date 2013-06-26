from pygame import *
from geometry import worldToScreen

class nSprite(object):
    def __init__(self):
        self.image = None
        self.pos = None
        self.size = None

    def getSize(self):
        if self.image == None:
            return self.size
        else:
            return self.image.get_size()

    def getRect(self):
        #if self.image == None or self.pos == None:
         #   print("Warning: Not enough info to generate sprite rect")
          #  return None

        return Rect(self.pos, self.getSize())

    def getRectScreen(self, game):
        rect = self.getRect()
        if rect == None:
            return None

        rect.x, rect.y = worldToScreen(rect.topleft, game.getView())
        return rect

    def draw(self, screen, game):
        if self.image == None:
            print("Warning: Attempting to draw sprite without image")
            return

        if self.pos == None:
            print("Warning: Attempting to draw sprite without posistion")
            return

        screen.blit(self.image, self.getRectScreen(game))

    def onCollision(self):
        return False
