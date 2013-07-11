from pygame import *
import math

from weapon import *
from config import *
from sprite import *
from textureset import *

class Player(nSprite):
    def __init__(self, pos):
        nSprite.__init__(self)
        self.pos = pos
        self.size = (32,32)

        self.textures = TextureSet("player.png", (0,64,128))

        self.facingAngle = 0

        self.weapons = [ WeaponFactory("pistol") ]
        self.maxHealth = 10.0
        self.health = self.maxHealth

        self.hasMoved = False

    def takeDamage(self, damage):
        self.health -= damage

        if self.health < 0:
            self.health = 0

    def setFacing(self, mouseCoords, game):
        (x1, y1) = self.getRectScreen(game).center
        (x2, y2) = mouseCoords

        dX = x1 - x2
        dY = y1 - y2

        self.facingAngle = math.atan2(dY * -1, dX * -1)

    def fireWeapon(self, numTicks):
        retVal = self.weapons[0].fire(self.getRect().center, self.facingAngle, numTicks)
        
        if self.weapons[0].isDepleted():
            self.weapons.pop(0)

        return retVal

    def move(self, xMove, yMove, worldMap):
        if self.hasMoved or (xMove == 0 and yMove == 0):
            return 

        tmpRect = self.getRect()
        
        xMove *= PLAYERMOVE
        yMove *= PLAYERMOVE
        tmpRect.move_ip(xMove, yMove)

        if worldMap.isAllowedPosition(tmpRect, True) and not worldMap.mobPresent(tmpRect):
            self.pos = tmpRect.topleft
            self.hasMoved = True
    

    def draw(self, screen, game, numTicks = 0):
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
        #screen.fill((255,0,0), rectScreen)
        self.image = self.textures.getSeriesRotated((0,0), self.size, (0,0), (self.facingAngle + 1.57) * -1)
        nSprite.draw(self, screen, game)
        self.hasMoved = False

        
