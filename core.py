# core.py: The Core class, contains the main loop and calls relevant methods in active mode when the time is right
# Author: Niklas Hedlund

from pygame import *
import sys, math

class Core(object):
    def __init__(self, resolution, fullscreen, drawFPS = False):
        self.activeMode = None
        self.lastMode = None

        self.runLoop = True
        self.res = resolution
        self.useFullscreen = fullscreen
        self.screen = None
        self.clock = None

        self.drawFPS = drawFPS
        self.numFrames = 0
        
    #Set mode as active and pass the old one to a variable
    def setActiveMode(self, newMode, discard=False):
        if self.activeMode != None:
            self.activeMode.onSwitchOut(self)

        if not discard:
            self.lastMode = self.activeMode
        
        newMode.onSwitchIn(self)
        self.activeMode = newMode

    #Restore the last mode
    def revertLastMode(self):
        if self.lastMode == None:
            return None

        self.activeMode.onSwitchOut(self)
        tmp = self.activeMode
        self.activeMode = self.lastMode
        self.activeMode.onSwitchIn(self)
        self.lastMode = tmp

        return tmp

    def doInit(self):
        #Initialize PyGame
        init()

        if self.useFullscreen:
            self.screen = display.set_mode(self.res, FULLSCREEN)
        else:
            self.screen = display.set_mode(self.res)

        self.fpsFont = font.Font(None, 20)

    #Tells the active mode to prepare for exit and then halts the game loop
    def pleaseExit(self):
        if self.activeMode.onQuit():
            self.runLoop = False

    def enterLoop(self):
        if self.screen == None:
            raise Exception("Screen not set, pygame not initialized")
        
        if self.activeMode == None:
            raise Exception("Critical: No mode set, nothing to do!")

        lastDraw = 0
        while self.runLoop:
            if time.get_ticks() - lastDraw > (1000.0 / self.activeMode.fps):
                #Time to draw

                #Calculate the current fps
                fps = math.floor(1 / (float(time.get_ticks() - lastDraw) / 1000.0))

                lastDraw = time.get_ticks()

                self.activeMode.onPreDraw(self, time.get_ticks())
                self.activeMode.onDraw(self.screen, self, time.get_ticks())
                
                if self.drawFPS:
                    fpsSurf = self.fpsFont.render(str(fps), False, (255,0,0))
                    self.screen.blit(fpsSurf, (20,20))

                display.update()
            else:
                #Not time for draw yet, lets do other stuff while we wait
                for e in event.get():
                    if e.type == QUIT:
                        if self.activeMode.onQuit():
                            self.runLoop = False
                            break
                    else:
                        self.activeMode.handleEvent(e, self, time.get_ticks())
            
                self.activeMode.onComputations(self, time.get_ticks())
            

        #Pygame quit
        quit()
