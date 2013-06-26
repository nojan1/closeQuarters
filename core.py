from pygame import *

class Core(object):
    def __init__(self, resolution, fullscreen):
        self.activeMode = None
        self.lastMode = None

        self.runLoop = True
        self.res = resolution
        self.useFullscreen = fullscreen
        self.screen = None
        self.clock = None

    def setActiveMode(self, newMode, discard=False):
        if not discard:
            self.lastMode = self.activeMode
        
        self.activeMode = newMode

    def revertLastMode(self):
        if self.lastMode == None:
            return None

        tmp = self.activeMode
        self.activeMode = self.lastMode
        self.lastMode = tmp

        return tmp

    def doInit(self):
        #Initialize PyGame
        init()

        if self.useFullscreen:
            self.screen = display.set_mode(self.res, FULLSCREEN)
        else:
            self.screen = display.set_mode(self.res)

        self.clock = time.Clock()

    def pleaseExit(self):
        if self.activeMode.onQuit():
            self.runLoop = False

    def enterLoop(self):
        if self.screen == None:
            raise Exception("Screen not set, pygame not initialized")
        
        if self.activeMode == None:
            raise Exception("Critical: No mode set, nothing to do!")

        lastDraw = 0
        numTicks = 0
        while self.runLoop:
            numTicks += time.get_ticks()

            if numTicks - lastDraw > (1000.0 / self.activeMode.fps):
                lastDraw = numTicks
                self.activeMode.onDraw(self.screen, self)
                display.update()
            else:
                self.activeMode.onPreEventCheck(self, numTicks)

                for e in event.get():
                    if e.type == QUIT:
                        if self.activeMode.onQuit():
                            self.runLoop = False
                            break
                    else:
                        self.activeMode.handleEvent(e, self, numTicks)
            
                self.activeMode.onPostEventCheck(self, numTicks)
            

        #Pygame quit
        quit()


