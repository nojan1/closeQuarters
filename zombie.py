from sprite import *
from config import *
import math

class Zombie(nSprite):
    def __init__(self, pos, ai):
        nSprite.__init__(self)
        self.pos = pos
        self.size = (20,20)

        self.ai = ai

        self.hasActivated = False

    def draw(self, screen, game):
        rectScreen = self.getRectScreen(game)

        #Draw mob
        screen.fill((100,0,200), rectScreen)
        self.hasActivated = False

    def takeDamage(self, damage):
        #True = Dead, False = "Took it like a man"
        return True


    def onActivation(self, game):
        if self.hasActivated:
            return

        self.hasActivated = True
        path = self.ai.canSeePlayer(self, game)
        if path:
            if path[1] < ATTACKTHRESHOLD:
                #Attack player
                pass
            else:
                newX = int(math.cos(path[0]) * ZOMBIEMOVE) + self.pos[0]
                newY = int(math.sin(path[0]) * ZOMBIEMOVE) + self.pos[1]
                
                self.pos = (newX, newY)
