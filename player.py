from pygame import *
import math

from weapon import *
from config import *
from sprite import *

class Player(nSprite):
    def __init__(self, pos):
        nSprite.__init__(self)
        self.pos = pos
        self.size = (30,30)

        self.facingAngle = 20

        self.weapons = [ WeaponFactory("pistol") ]

    def setFacing(self, mouseCoords, game):
        (x1, y1) = self.getRectScreen(game).center
        (x2, y2) = mouseCoords

        dX = x1 - x2
        dY = y1 - y2

        self.facingAngle = math.atan2(dY * -1, dX * -1)

    def fireWeapon(self):
        retVal = self.weapons[0].fire(self.getRect().center, self.facingAngle)
        
        if self.weapons[0].isDepleted():
            self.weapons.pop(0)

        return retVal

    def move(self, xMove, yMove, worldMap):
        tmpRect = self.getRect()
        
        xMove *= PLAYERMOVE
        yMove *= PLAYERMOVE
        tmpRect.move_ip(xMove, yMove)

        if worldMap.isAllowedPosition(tmpRect):
            self.pos = tmpRect.topleft

    def draw(self, screen, game):
        rectScreen = self.getRectScreen(game)
        #Draw targeter, circle
        draw.circle(screen, (0,255,0), rectScreen.center, rectScreen.width, 1) 
        
        #Line...
        x1 = int(math.cos(self.facingAngle) * (rectScreen.width / 1.3)) + rectScreen.center[0]
        y1 = int(math.sin(self.facingAngle) * (rectScreen.width / 1.3)) + rectScreen.center[1]
        
        x2 = int(math.cos(self.facingAngle) * (rectScreen.width * 1.2)) + rectScreen.center[0]
        y2 = int(math.sin(self.facingAngle) * (rectScreen.width * 1.2)) + rectScreen.center[1]
        
        draw.aaline(screen, (0,255,0), (x1, y1), (x2, y2), 1)

        #Draw character
        screen.fill((255,0,0), rectScreen)

        
