# menu.py: The main menu, inherits Mode
# Provides the user with a series off buttons and is used to start / end the game but also as a pause menu
# Author: Niklas Hedlund

from pygame import *
import os

from mode import Mode
from config import *    
from game import Game
from instructions import InstructionsScreen

class MenuButton(object):
    def __init__(self, text, onClick):
        self.text = text
        self.onClick = onClick

        self.glowImage = image.load(os.path.join(GRAPHICPATH, "menu_glow.png"))
        self.buttonImage = image.load(os.path.join(GRAPHICPATH, "menu_button.png"))

    def getRect(self, core, index):
        x = (core.res[0] / 2) - (BUTTONSIZE[0] / 2)
        y = BUTTONOFFSETY + ((BUTTONSIZE[1] + BUTTONSPACINGY) * index)

        return Rect(x, y, BUTTONSIZE[0], BUTTONSIZE[1])

    def drawGlow(self, screen, core, index):
        rect = self.getRect(core, index)
        rect.x -= 5
        rect.y -= 5
        rect.width += 10
        rect.height += 10

        #draw.rect(screen, (255,0,0), rect)
        screen.blit(self.glowImage, rect)

    def draw(self, screen, core, index):
        rect = self.getRect(core, index)
        fonten = font.Font(None, BUTTONSIZE[1] - 5)
        fontText = fonten.render(self.text, True, (255,255,255))

        #draw.rect(screen, (0,0,255), rect)
        screen.blit(self.buttonImage, rect)
        screen.blit(fontText, ((rect.x + (rect.width / 2) - (fontText.get_width() / 2)),(rect.y + (rect.height / 2) - (fontText.get_height() / 2))))

class Menu(Mode):
    def __init__(self, core):
        Mode.__init__(self, core, 30)

        self.menuButtons = [MenuButton("Start New Game", self.onStartGameClick),
                            MenuButton("Instructions", self.onInstructionsClick),
                            MenuButton("Exit", self.onExitClick)]
        self.activeButton = 0

        self.backdrop = image.load(os.path.join(GRAPHICPATH, "menu_backdrop.jpg"))
        self.menuSound = mixer.Sound(os.path.join(SOUNDPATH, "menu_click.wav"))

    def onResumeGame(self, core):
        core.revertLastMode()

    def onStartGameClick(self, core):
        if self.menuButtons[0].text != "Resume Game":
            self.menuButtons.insert(0, MenuButton("Resume Game", self.onResumeGame))
            
        core.setActiveMode( Game(core) )
        
    def onInstructionsClick(self, core):
        core.setActiveMode( InstructionsScreen(core) )

    def onExitClick(self, core):
        core.pleaseExit()

    def onDraw(self, screen, core, numTicks):
        backdropX = (core.res[0] / 2) - (self.backdrop.get_width() / 2)

        screen.fill((0,0,0))
        screen.blit(self.backdrop, (backdropX,0))

        self.menuButtons[self.activeButton].drawGlow(screen, core, self.activeButton)
        for i, b in enumerate(self.menuButtons):
            b.draw(screen, core, i)

    def handleEvent(self, e, core, numTicks):
        if e.type == KEYDOWN:
            if e.key == K_UP:
                self.activeButton -= 1
                if self.activeButton < 0:
                    self.activeButton = len(self.menuButtons) - 1

                self.menuSound.play()
            elif e.key == K_DOWN:
                self.activeButton += 1
                if self.activeButton > len(self.menuButtons) - 1:
                    self.activeButton = 0

                self.menuSound.play()  
            elif e.key == K_RETURN:
                self.menuButtons[self.activeButton].onClick(core)
