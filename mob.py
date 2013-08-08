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

        #Mob standard attributes
        self.ai = ai
        self.health = health
        self.damage = damage
        self.speed = speed

        #For AI
        self.hasSeenPlayer = False
        self.hasActivated = False
        self.lastAttack = 0

        #Which imageIndes should be used in the animation for different rotations
        self.imageIndexesTable = []

        self.facingAngle = 0

    def takeDamage(self, damage):
        #Return values: True = Dead, False = "Took it like a man"
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
        #If the Mob has been seen the player will be in search and destroy mode
        if self.hasSeenPlayer:
            self.animEnable = True
            #Find path and attack!
            newPos = self.ai.findPath(self, game)
            if newPos:
                attackRect = Rect(newPos, self.size)
                attackRect.move_ip(ATTACKTHRESHOLD / 2, ATTACKTHRESHOLD / 2)
                attackRect.inflate_ip(ATTACKTHRESHOLD, ATTACKTHRESHOLD)

                if game.player.getRect().colliderect( attackRect ):
                    #Attack player
                    if tickCount - self.lastAttack > 500:
                        game.handlePlayerDamage(self.damage)
                        self.lastAttack = tickCount
                else:
                    self.facingAngle = geometry.getAngleDistance(self.pos, newPos)[0]
                    self.pos = newPos

                    if len(self.imageIndexesTable) != 0:
                        #Switch to another set of textures depending on current angle (handles rotation)
                        #Divides a circle into correct number of slices
                        slices = 360.0 / len(self.imageIndexesTable)
                        angle = math.degrees(self.facingAngle)
                        #The index is which of the different slices that the mob facing angle is currently in
                        index = int(round(angle / slices)) % len(self.imageIndexesTable)
                
                        self.imageIndexes = self.imageIndexesTable[index]

            else:
                #No valid path was found = Mob standing still
                self.animEnable = False
        else:
            self.hasSeenPlayer = self.ai.canSeePlayer(self, game) != False
     
