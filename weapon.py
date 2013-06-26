from geometry import *
from config import *
import math
import os

from pygame import *

def WeaponFactory(name):
    weapons = {"pistol": Pistol, "autorifle": AutoRifle, "laser": Laser}    
    return weapons[name]()

class Bullet(object):
    def __init__(self, pos, angle, speed = 10):
        self.pos = pos
        self.angle = angle
        self.speed = speed

        self.hasMoved = False

    def move(self):
        if self.hasMoved:
            return

        newX = int(math.cos(self.angle) * self.speed) + self.pos[0]
        newY = int(math.sin(self.angle) * self.speed) + self.pos[1]

        self.pos = (newX, newY)
        self.hasMoved = True

    def hitMob(self, map):
        selfRect = Rect(self.pos, (1,1))
        for m in map.mobs:
            if selfRect.colliderect(m.getRect()):
                return m

        return False

    def hitWall(self, map):
        selfRect = Rect(self.pos, (1,1))
        return not map.isAllowedPosition(selfRect)

    def draw(self, screen, game):
        screen.fill((0,0,0), Rect(worldToScreen(self.pos, game.getView()), (3,3)))
        self.hasMoved = False

class Weapon(object):
    def __init__(self):
        self.groundImage = None
        self.HUDImage = None

        self.damage = 0
        self.rof = 0

        self.bulletClass = Bullet
        self.lastFire = 0

    def isDepleted(self):
        return False

    def fire(self, startPos, angle, numTicks):
        if self.rof == 0:
            raise NotImplementedError("ROF is zero = Not proper weapon")

        if numTicks - self.lastFire > (1000.0 / self.rof):
            self.lastFire = numTicks
            return self.bulletClass(startPos, angle)
        else:
            return None


class Pistol(Weapon):
    def __init__(self):
        Weapon.__init__(self)

        self.HUDImage = image.load(os.path.join(GRAPHICPATH, "pistol.png"))

        self.damage = 1
        self.rof = 1.5

class AutoRifle(Weapon):
    pass

class Laser(Weapon):
    pass
