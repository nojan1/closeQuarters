from pygame import *

from mode import *
from menu import *

class GameOverScreen(Mode):
    def __init__(self, game):
        Mode.__init__(self, game.core, 30)
        self.game = game

        self.lastScreen = game.core.screen

    def onDraw(self, screen, core):
        screen.blit(self.lastScreen, (0,0))
        
        screen.fill((100,100,100,100), Rect(300,40,424,668))

    def handleEvent(self, event, core, numTicks):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                core.setActiveMode( Menu(core) )
