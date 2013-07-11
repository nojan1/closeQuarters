from mob import *

class Spider(Mob):
    def __init__(self, pos, ai, texture):
        Mob.__init__(self, ai, 3, 2)
        self.pos = pos
        self.size = (64,32)

    def draw(self, screen, game, numTicks = 0):
        rectScreen = self.getRectScreen(game)

        #Draw mob
        screen.fill((0,100,0), rectScreen)
        self.hasActivated = False
