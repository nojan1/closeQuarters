from mob import *

class Zombie(Mob):
    def __init__(self, pos, ai):
        Mob.__init__(self, ai, 2, 1)
        self.pos = pos
        self.size = (25,25)

    def draw(self, screen, game, numTicks = 0):
        rectScreen = self.getRectScreen(game)

        #Draw mob
        screen.fill((100,0,200), rectScreen)
        self.hasActivated = False
