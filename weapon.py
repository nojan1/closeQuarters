from geometry import *
import math
from pygame import *

def WeaponFactory(name):
    weapons = {"pistol": Pistol, "autorifle": AutoRifle, "laser": Laser}    
    return weapons[name]()

class Bullet(object):
    def __init__(self, pos, angle, speed = 10):
        self.pos = pos
        self.angle = angle
        self.speed = speed

    def move(self):
        newX = int(math.cos(self.angle) * self.speed) + self.pos[0]
        newY = int(math.sin(self.angle) * self.speed) + self.pos[1]

        self.pos = (newX, newY)

    def hitMob(self, mobs):
        return False

    def hitWall(self, map):
        selfRect = Rect(self.pos, (1,1))
        return not map.isAllowedPosition(selfRect)

    def draw(self, screen, game):
        screen.fill((0,0,0), Rect(worldToScreen(self.pos, game.getView()), (2,2)))

class Weapon(object):
    def __init__(self):
        self.groundImage = None
        self.HUDImage = None

        self.damage = 0
        self.rof = 0

        self.bulletClass = Bullet

    def isDepleted(self):
        return False

    def fire(self, startPos, angle):
        return self.bulletClass(startPos, angle)


class Pistol(Weapon):
    def __init__(self):
        Weapon.__init__(self)

        self.damage = 1
        self.rof = 1

class AutoRifle(Weapon):
    pass

class Laser(Weapon):
    pass
