# mob.py: Base class for mobs, defines basic things such as health / damage but also contains the part where the AI system gets called
# Author: Niklas Hedlund 

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
            self.animEnable = True
            #Find path and attack!
            newPos = self.ai.findPath(self, game)
            if newPos:
                if game.player.getRect().colliderect( Rect(newPos, self.size) ):
                    #Attack player
                    if tickCount - self.lastAttack > 500:
                        game.handlePlayerDamage(self.damage)
                        self.lastAttack = tickCount
                else:
                    self.pos = newPos
            else:
                self.animEnable = False
        else:
            self.hasSeenPlayer = self.ai.canSeePlayer(self, game) != False
     
