import os
from pygame import *

from config import *

class HUD(object):
    def __init__(self, player):
        self.player = player

        self.baseImg = image.load(os.path.join(GRAPHICPATH, "main_section.png"))
        self.slideImg = image.load(os.path.join(GRAPHICPATH, "slide.png"))
        self.boxImg = image.load(os.path.join(GRAPHICPATH, "electric_textplate.png"))

        self.ammoFont = font.Font(None, 30)

    def draw(self, screen, game):
        mainRect = Rect((0,0), self.baseImg.get_size())
        mainRect.x = game.core.res[0] - mainRect.width + 43
        mainRect.y = game.core.res[1] - mainRect.height + 43

        barOffset = int(160.0 * (self.player.health / self.player.maxHealth))
        slideRect = Rect(mainRect.topright, self.slideImg.get_size())
        slideRect.move_ip(-512, (88 - barOffset))

        boxRect = Rect(mainRect.bottomleft, self.boxImg.get_size())
        boxRect.move_ip(-1, -510)

        weaponRect = Rect(boxRect.topleft, self.player.weapons[0].HUDImage.get_size())
        weaponRect.move_ip(305,419)

        textSurface = self.ammoFont.render(self.player.weapons[0].getHUDText(), True, (0,0,0))
        textRect = textSurface.get_rect()
        textRect.topleft = weaponRect.topleft
        textRect.move_ip(-60, 2)

        screen.blit(self.boxImg, boxRect)
        screen.blit(self.baseImg, mainRect) 
        screen.blit(self.slideImg, slideRect)
        screen.blit(self.player.weapons[0].HUDImage, weaponRect)
        screen.blit(textSurface, textRect)
