from pygame import *

from mode import Mode
from map import Map

class Game(Mode):
    def __init__(self, core):
        Mode.__init__(self, core, 50)

        self.map = Map()
        self.map.loadLevel(1)

    def getView(self):
        tmp = Rect(0, 0, self.core.res)
        
        #Center around player
        tmp.center = (100,100)

        if tmp.x < 0:
            tmp.x = 0

        if tmp.y < 0:
            tmp.y = 0
        
        return tmp

    def onDraw(self, screen, core):
        screen.fill((0,0,0))
        
    def handleEvent(self, event, core):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                core.revertLastMode()
            elif event.key == K_w:
                #Player move up
                pass
            elif event.key == K_s:
                #Player move down
                pass
            elif event.key == K_a:
                #Player move left
                pass
            elif event.key == K_d:
                #Player move right
                pass
