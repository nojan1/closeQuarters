# pickup.py: Defines the pickups, these are special types off tiles which will act in certain ways until they have been picked upp and afterwards reverting to just a piece of floor. All effects are set by the instances of pickups by themselves (game core does nothing in this case) 
# Author: Niklas Hedlund

from tile import Floor
from weapon import *
from config import *

from pygame import image, draw, rect
import os

class Pickup(Floor):
    def __init__(self, location, tileTextures, groundImage):
        Floor.__init__(self, location, tileTextures)
        
        self.groundImage = groundImage
        self.glowImage = image.load(os.path.join(GRAPHICPATH, "pickup_glow.png"))
        self.used = False

    def draw(self, screen, game, numTicks = 0):
        Floor.draw(self, screen, game, numTicks)
        
        if not self.used:
            #Draw the pickup image on top of tile image
            rect = self.getRectScreen(game)
            
            screen.blit(self.glowImage, Rect(rect.topleft, (32,32)))
            screen.blit(self.groundImage, rect)
            
            #draw.circle(screen, (0, 0, 150), rect.center, int(rect.width * 0.6), 1) 

    def onCollision(self, game, isPlayer):
        if not isPlayer or self.used:
            return False

        return self.onPickup(game)

    def onPickup(self, game):
        return False

class WeaponPickup(Pickup):
    def __init__(self, location, tileTextures, weaponObj):
        Pickup.__init__(self, location, tileTextures, weaponObj.groundImage)

        self.weaponObj = weaponObj

    def onPickup(self, game):
        game.player.weapons.insert(0, self.weaponObj)
        self.used = True
        return False

class HealthPickup(Pickup):
    def __init__(self, location, tileTextures):
         groundImage = image.load(os.path.join(GRAPHICPATH, "health_pickup.png"))
         Pickup.__init__(self, location, tileTextures, groundImage)

    def onPickup(self, game):
        game.player.health += 2.5
        if game.player.health > game.player.maxHealth:
            game.player.health = game.player.maxHealth

        self.used = True
        return False
