from tile import Floor
from weapon import *

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

    def onCollision(self, game):
        if self.used:
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
