# mob.py: Base class for mobs, defines basic things such as health / damage but also contains the part where the AI system gets called
# Author: Niklas Hedlund 

from animsprite import *
from config import *
import geometry
import math
import random

class Mob(AnimSprite):
    def __init__(self, ai, health, damage, speed):
        AnimSprite.__init__(self)

        self.ai = ai
        self.health = health
        self.damage = damage
        self.speed = speed

        self.hasSeenPlayer = False
        self.hasActivated = False
        self.lastAttack = 0

        self.imageIndexesTable = []
        self.facingAngle = 0

    def takeDamage(self, damage):
        #True = Dead, False = "Took it like a man"
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return True

        return False

    def draw(self, screen, game, numTicks = 0):
        self.hasActivated = False
        AnimSprite.draw(self, screen, game, numTicks)

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
                    self.facingAngle = geometry.getAngleDistance(self.pos, newPos)[0]
                    self.pos = newPos

                    if len(self.imageIndexesTable) != 0:
                        #Switch to another set of textures depending on current angle
                        slices = 360.0 / len(self.imageIndexesTable)
                        angle = math.degrees(self.facingAngle)
                        index = int(round(angle / slices)) % len(self.imageIndexesTable)
                
                        self.imageIndexes = self.imageIndexesTable[index]

            else:
                self.animEnable = False
        else:
            self.hasSeenPlayer = self.ai.canSeePlayer(self, game) != False
     
