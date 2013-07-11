from animsprite import *
from config import *
import math
import random

class Mob(AnimSprite):
    def __init__(self, ai, health, damage):
        AnimSprite.__init__(self)

        self.ai = ai
        self.health = health
        self.damage = damage

        self.hasSeenPlayer = False
        self.hasActivated = False
        self.lastAttack = 0

    def takeDamage(self, damage):
        #True = Dead, False = "Took it like a man"
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return True

        return False

    def onActivation(self, game, tickCount):
        if self.hasActivated:
            return

        self.hasActivated = True
        if self.hasSeenPlayer:
            #Find path and attack!
            path = self.ai.findPath(self, game)
            if path:
                if path[1] < ATTACKTHRESHOLD:
                    #Attack player
                    if tickCount - self.lastAttack > 500:
                        game.handlePlayerDamage(self.damage)
                        self.lastAttack = tickCount
                else:
                    newX = int(math.cos(path[0]) * ZOMBIEMOVE) + self.pos[0]
                    newY = int(math.sin(path[0]) * ZOMBIEMOVE) + self.pos[1]
                
                    self.pos = (newX, newY)
        else:
            self.hasSeenPlayer = self.ai.canSeePlayer(self, game) != False
            self.animEnable = True
     
