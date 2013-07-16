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

        self.fireSound = None

    def getHUDText(self):
        return ""
        
    def isDepleted(self):
        return False

    def fire(self, startPos, angle, numTicks, channel):
        if self.rof == 0:
            raise NotImplementedError("ROF is zero = Not proper weapon")

        if numTicks - self.lastFire > (1000.0 / self.rof):
            if self.fireSound != None:
                channel.play(self.fireSound)

            self.lastFire = numTicks
            return self.bulletClass(startPos, angle)
        else:
            return None


class Pistol(Weapon):
    def __init__(self):
        Weapon.__init__(self)

        self.HUDImage = image.load(os.path.join(GRAPHICPATH, "pistol.png"))
        self.fireSound = mixer.Sound(os.path.join(SOUNDPATH, "barreta_m9.wav"))
        self.fireSound.set_volume(0.8)

        self.damage = 1
        self.rof = 1.5

    def getHUDText(self):
        return "INF"

class AutoRifle(Pistol):
    def __init__(self):
        Pistol.__init__(self)

        self.HUDImage = image.load(os.path.join(GRAPHICPATH, "rifle.png"))
        self.groundImage = image.load(os.path.join(GRAPHICPATH, "rifle_ground.png"))

        self.rof = 8
        self.shotsRemaining = 100

    def fire(self, startPos, angle, numTicks, channel):
        retVal = Pistol.fire(self, startPos, angle, numTicks, channel)
        if retVal != None:
            self.shotsRemaining -= 1
            
        return retVal

    def isDepleted(self):
        return self.shotsRemaining <= 0 

    def getHUDText(self):
        return str(self.shotsRemaining)

class Laser(Weapon):
    def __init__(self):
        Weapon.__init__(self)

        self.bulletClass = LaserBullet

        self.HUDImage = image.load(os.path.join(GRAPHICPATH, "rifle.png"))
        self.groundImage = image.load(os.path.join(GRAPHICPATH, "LaserGun.gif"))

        self.fireSound = mixer.Sound(os.path.join(SOUNDPATH, "laser.wav"))
        self.fireSound.set_volume(0.8)

        self.damage = 2
        self.rof = 1

        self.stressLevel = 0

    def fire(self, startPos, angle, numTicks, channel):
        if not Weapon.fire(self, startPos, angle, numTicks, channel):
            return

        #To much firing overheats weapon1
        if numTicks - self.lastFire < LASERTHRESHOLD:
            self.stressLevel += 1
        else:
            self.stressLevel -= 1       

        #Make sure the value is between limits
        if self.stressLevel < 0:
            self.stressLevel = 0
        elif self.stressLevel > 4:
            self.stressLevel = 4

    def getHUDText(self):
        labels = ["COLD", "OKEY", "HOT", "BURN", "OVER"]
        return labels[self.stressLevel]

    def isDepleted(self):
        return self.stressLevel == 4

class LaserBullet(Bullet):
    def __init__(self, pos, angle, speed = 10):
        Bullet.__init__(self, pos, angle, speed)

    def draw(self, screen, game):
        self.hasMoved = False

        pos = worldToScreen(self.pos, game.getView())

        x1 = math.cos(self.angle) * -5 + pos[0] 
        y1 = math.cos(self.angle) * -5 + pos[1]

        x2 = math.cos(self.angle) * 3 + pos[0]
        y2 = math.sin(self.angle) * 3 + pos[1]

        draw.line(screen, (200,0,0), (x1, y1), (x2, y2), 1)
        
