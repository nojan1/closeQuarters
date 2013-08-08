# gameover.py: The game over screen inherits Mode and is responsible for showing the player the end of game information
# Author: Niklas Hedlund

from pygame import *
import os

from config import *
from mode import Mode
import menu

class GameOverScreen(Mode):
    def __init__(self, game, playerWon = False):
        Mode.__init__(self, game.core, 30)
        self.game = game
        self.playerWon = playerWon

        #Save the last screen drawn by the core, this will be used as the background to give the illusion of a floating menu
        self.lastScreen = game.core.screen

        if self.playerWon:
            filenameSound = "win.ogg"
            filenameTopic = "topic_won.png"
        else:
            filenameSound = "lose.ogg"
            filenameTopic = "topic_lost.png"

        self.music = mixer.Sound(os.path.join(SOUNDPATH, filenameSound))
        self.music.play(loops=-1, fade_ms=300)

        self.imageTopic = image.load(os.path.join(GRAPHICPATH, filenameTopic))
        self.imageFrame = image.load(os.path.join(GRAPHICPATH, "endgame_frame.png"))

        self.fontHeader = font.Font(None, 70)
        self.fontContent = font.Font(None, 50)

    def drawTexts(self, screen, startPos, texts, spacing = 20):
        pos = startPos
        
        for text in texts:
            screen.blit(text, pos)
            pos = (pos[0], pos[1] + spacing + text.get_height())

    def onDraw(self, screen, core, numTicks):
        screen.blit(self.lastScreen, (0,0))
        
        #Center texts
        frameRect = Rect((0, 120), self.imageFrame.get_size())
        frameRect.x = (core.res[0] / 2) - (frameRect.width / 2)

        topicRect = Rect((0, 10), self.imageTopic.get_size())
        topicRect.x = (core.res[0] / 2) - (topicRect.width / 2)

        screen.blit(self.imageTopic, topicRect)
        
        #Calculate statistics
        if self.game.shotsFired == 0:
            accuracy = 0
        else:
            accuracy = int((float(self.game.shotsHit) / float(self.game.shotsFired)) * 100.0)

        #Prepare rendered fonts
        header = self.fontHeader.render("Statistics", True, (0,0,0))
        line1 = self.fontContent.render("Shots fired: %i" % self.game.shotsFired, True, (0,0,0))
        line2 = self.fontContent.render("Shots hit: %i" % self.game.shotsHit, True, (0,0,0))
        line3 = self.fontContent.render("Accuracy: %i percent" % accuracy, True, (0,0,0))

        screen.blit(self.imageFrame, frameRect)
        #Draw the fonts
        self.drawTexts(screen, frameRect.move(20,20).topleft, [header, line1, line2, line3])

    def handleEvent(self, event, core, numTicks):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.music.stop()
                core.setActiveMode( menu.Menu(core) )
