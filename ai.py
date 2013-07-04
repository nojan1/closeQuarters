import math
from pygame import Rect

from config import *

class AI(object):
    def __init__(self):
        #Used to speed up calculations on the expense of memory...
        self.rectCache = []

    def canSeePlayer(self, mob, game):
        return self.isClearLine(mob.getRect().center, game.player.getRect().center, game, False)

    def getAngleDistance(self, source, destination):
        x1, y1 = source
        x2, y2 = destination

        dX = x1 - x2
        dY = y1 - y2

        angle = math.atan2(dY * -1, dX * -1)
        distance = math.sqrt((dX*dX) + (dY*dY))
        
        return (angle, distance)

    def isClearLine(self, source, destination, game, mobsBlockLOS = True):
        #Return False or (angle, distance)
        x1, y1 = source
        x2, y2 = destination
        angle, distance = self.getAngleDistance(source, destination)

        increment = 0
        while increment <= (distance - (TILESIZE[0] / 2)):
            increment += TILESIZE[0] / 2.0
            
            x = int(math.cos(angle) * increment) + x1
            y = int(math.sin(angle) * increment) + y1

            rectToCheck = Rect((x,y), (TILESIZE[0] / 2, TILESIZE[1] / 2))
            #if rectToCheck.collidelist(self.rectCache) != -1:
             #   continue

            if (not game.map.isAllowedPosition(rectToCheck)) or (mobsBlockLOS and game.map.mobPresent(rectToCheck)):
                return False
            else:
                self.rectCache.append(rectToCheck)
                
        return (angle, distance)

    def findPath(self, mob, game):
        #Return valid move on a path leading to player
        destination = game.player.getRect()
        source = mob.getRect()
        destination.size = source.size

        baseAngle, distance = self.getAngleDistance(source.center, destination.center)
        angle = baseAngle

        angleModifiers = [math.radians(x) for x in [20, -20, 40, -40, 60, -60, 80, -80]]

        while self.isClearLine(source.center, destination.center, game, True) == False:
            if len(angleModifiers) == 0:
                print("Found no path")
                return False

            angle = baseAngle + angleModifiers.pop(0)

            destination.x = int(math.cos(angle) * ZOMBIEMOVE) + source.x 
            destination.y = int(math.sin(angle) * ZOMBIEMOVE) + source.y 

        return (angle, distance)
