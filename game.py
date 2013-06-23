from pygame import *

from mode import Mode
from map import Map
from player import Player

class Game(Mode):
    def __init__(self, core):
        Mode.__init__(self, core, 50)

        self.map = Map()
        self.map.loadLevel(1)

        self.player = Player((200,200))

    def getView(self):
        tmp = Rect((0, 0), tuple(self.core.res))
        #Center around player
        tmp.center = self.player.pos

        if tmp.x < 0:
            tmp.x = 0

        if tmp.y < 0:
            tmp.y = 0
        
        return tmp

    def onDraw(self, screen, core):
        screen.fill((0,0,0))

        self.map.drawTilesInView(screen, self)
        self.player.draw(screen, self)

    def onPostEventCheck(self, core):
        states = key.get_pressed()
        if states[K_w]:
            #Player move up
            self.player.move(0,-1, self.map)
        if states[K_s]:
            #Player move down
            self.player.move(0,1, self.map)
        if states[K_a]:
            #Player move left
            self.player.move(-1,0, self.map)
        if states[K_d]:
            #Player move right
            self.player.move(1,0, self.map)

    def handleEvent(self, event, core):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                core.revertLastMode()
