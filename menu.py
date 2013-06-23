from pygame import *
import os

from mode import Mode
from config import *    
from game import Game

class MenuButton(object):
    def __init__(self, index, text, onClick):
        self.index = index
        self.text = text
        self.onClick = onClick

    def getRect(self, core):
        x = (core.res[0] / 2) - (BUTTONSIZE[0] / 2)
        y = BUTTONOFFSETY + ((BUTTONSIZE[1] + BUTTONSPACINGY) * self.index)

        return Rect(x, y, BUTTONSIZE[0], BUTTONSIZE[1])

    def drawGlow(self, screen, core):
        rect = self.getRect(core)
        rect.x -= 5
        rect.y -= 5
        rect.width += 10
        rect.height += 10

        draw.rect(screen, (255,0,0), rect)

    def draw(self, screen, core):
        rect = self.getRect(core)
        fonten = font.Font(None, BUTTONSIZE[1] - 5)
        fontText = fonten.render(self.text, True, (255,255,255))

        draw.rect(screen, (0,0,255), rect)
        screen.blit(fontText, ((rect.x + (rect.width / 2) - (fontText.get_width() / 2)),(rect.y + (rect.height / 2) - (fontText.get_height() / 2))))

class Menu(Mode):
    def __init__(self, core):
        Mode.__init__(self, core, 30)

        self.menuButtons = [MenuButton(0, "Start New Game", self.onStartGameClick),
                            MenuButton(1, "Highscore", self.onHighscoreClick),
                            MenuButton(2, "Options", self.onOptionsClick),
                            MenuButton(3, "Exit", self.onExitClick)]
        self.activeButton = 0

        #self.backdrop = image.load(os.path.join(GRAPHICSPATH, "menu_backdrop.jpg"))

    def onStartGameClick(self, core):
        if self.menuButtons[0].text == "Resume Game":
            core.revertLastMode()
        else:  
            self.menuButtons[0].text = "Resume Game"
            core.setActiveMode( Game(core) )
        

    def onHighscoreClick(self, core):
        pass

    def onOptionsClick(self, core):
        pass

    def onExitClick(self, core):
        core.pleaseExit()

    def onDraw(self, screen, core):
        fonten = font.Font(None, 40)
        
        screen.fill((0,0,0))
        #screen.blit(self.backdrop, (0,0))
        screen.blit(fonten.render("Close Quarters! Shoot that zombie...", True, (255,255,255)), (170,80))

        self.menuButtons[self.activeButton].drawGlow(screen, core)
        for b in self.menuButtons:
            b.draw(screen, core)


    def handleEvent(self, e, core):
        if e.type == KEYDOWN:
            if e.key == K_UP:
                self.activeButton -= 1
                if self.activeButton < 0:
                    self.activeButton = len(self.menuButtons) - 1
            elif e.key == K_DOWN:
                self.activeButton += 1
                if self.activeButton > len(self.menuButtons) - 1:
                    self.activeButton = 0
            elif e.key == K_RETURN:
                self.menuButtons[self.activeButton].onClick(core)
