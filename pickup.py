from tile import Floor
from weapon import *
from config import *

from pygame import image
import os

class Pickup(Floor):
    def __init__(self, location, tileTextures, groundImage):
        Floor.__init__(self, location, tileTextures)
        
        self.groundImage = groundImage
        self.used = False

    def draw(self, screen, game, numTicks = 0):
        Floor.draw(self, screen, game, numTicks)
        
        if not self.used:
            #Draw the pickup image on top of tile image
            screen.blit(self.groundImage, self.getRectScreen(game))

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
