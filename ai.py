# ai.py: The AI system, does line of sight calulations as well as some path finding (not implemented yet)
# Author: Niklas Hedlund

import math
from pygame import Rect

from config import *
from geometry import getAngleDistance

class AI(object):
    def canSeePlayer(self, mob, game):
        return self.isClearLine(mob.getRect().center, game.player.getRect().center, game, False)

    def isClearLine(self, source, destination, game, mobsBlockLOS = True):
        #Return False or (angle, distance)
        x1, y1 = source
        x2, y2 = destination
        angle, distance = getAngleDistance(source, destination)

        increment = 0
        while increment <= (distance - (TILESIZE[0] / 2)):
            increment += TILESIZE[0] / 2.0
            
            x = int(math.cos(angle) * increment) + x1
            y = int(math.sin(angle) * increment) + y1

            rectToCheck = Rect((x,y), (TILESIZE[0] / 2, TILESIZE[1] / 2))

            if (not game.getMap().isAllowedPosition(rectToCheck)) or (mobsBlockLOS and game.getMap().mobPresent(rectToCheck)):
                return False
                
        return (angle, distance)

    def findPath(self, mob, game):
        #Return valid move on a path leading to player
        destination = game.player.getRect()
        source = mob.getRect()
        destination.size = source.size

        path = self.canSeePlayer(mob, game)
        if path:
            #Direct line of sight to player... no need to find a path
            x = int(math.cos(path[0]) * mob.speed) + source.x
            y = int(math.sin(path[0]) * mob.speed) + source.y
            return (x,y)
        else:
            #Go into search mode (Not implemented)
            initialAngle = getAngleDistance(source.center, destination.center)[0] - math.radians(90)
            return self.search(source, destination, game, initialAngle)

    def search(self, source, destination, game, angle):
        return False
        
