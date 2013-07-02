from sprite import *
from config import *
import math
import random

class Zombie(nSprite):
    def __init__(self, pos, ai):
        nSprite.__init__(self)
        self.pos = pos
        self.size = (25,25)

        self.ai = ai

        self.hasActivated = False
        self.lastAttack = 0
        
    def draw(self, screen, game):
        rectScreen = self.getRectScreen(game)

        #Draw mob
        screen.fill((100,0,200), rectScreen)
        self.hasActivated = False

    def takeDamage(self, damage):
        #True = Dead, False = "Took it like a man"
        return True


    def onActivation(self, game, tickCount):
        if self.hasActivated:
            return

        self.hasActivated = True
        path = self.ai.canSeePlayer(self, game)
        if path:
            if path[1] < ATTACKTHRESHOLD:
                #Attack player
                if tickCount - self.lastAttack > 500:
                    game.handlePlayerDamage(1)
                    self.lastAttack = tickCount
            else:
                newX = int(math.cos(path[0]) * ZOMBIEMOVE) + self.pos[0]
                newY = int(math.sin(path[0]) * ZOMBIEMOVE) + self.pos[1]
                
                #if not game.map.mobPresent(Rect((newX, newY), self.size)):
                self.pos = (newX, newY)
