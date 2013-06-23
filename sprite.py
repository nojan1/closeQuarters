from pygame import *
from geometry import worldToScreen

class nSprite(object):
    def __init__(self):
        self.image = None
        self.pos = None

    def getRect(self):
        if self.image == None or self.pos == None:
            print("Warning: Not enough info to generate sprite rect")
            return None

        return Rect(self.pos, self.image.get_size())

    def getRectScreen(self, game):
        rect = self.getRect()
        if rect == None:
            return None

        x,y = worldToScreen((rect.x, rect.y), game.getView())
        rect.move_ip(x, y)
        return rect

    def draw(self, screen, game):
        if self.image == None:
            print("Warning: Attempting to draw sprite without image")
            return

        if self.pos == None:
            print("Warning: Attempting to draw sprite without posistion")
            return

        screen.blit(self.image, self.getRectScreen(game))
