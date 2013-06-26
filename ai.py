import math
from pygame import Rect

from config import *

class AI(object):
    def __init__(self):
        #Used to speed up calculations on the expense of memory...
        self.rectCache = []

    def canSeePlayer(self, zombie, game):
        #Return False or (angle, distance)
        x1 = zombie.getRect().center[0]
        y1 = zombie.getRect().center[1]
        x2 = game.player.getRect().center[0]
        y2 = game.player.getRect().center[1]

        dX = x1 - x2
        dY = y1 - y2

        angle = math.atan2(dY * -1, dX * -1)
        distance = math.sqrt((dX*dX) + (dY*dY))

        increment = 0
        while increment <= (distance - (TILESIZE[0] / 2)):
            increment += TILESIZE[0] / 2.0
            
            x = int(math.cos(angle) * increment) + x1
            y = int(math.sin(angle) * increment) + y1

            rectToCheck = Rect((x,y), (TILESIZE[0] / 2, TILESIZE[1] / 2))
            if rectToCheck.collidelist(self.rectCache) != -1:
                continue

            if not game.map.isAllowedPosition(rectToCheck):
                return False
            else:
                self.rectCache.append(rectToCheck)
                
        return (angle, distance)

    def findPath(self, zombie, game):
        #Return valid move on a path leading to player
        pass
