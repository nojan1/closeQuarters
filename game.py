from pygame import *

from mode import Mode
from map import Map
from player import Player
from hud import *

class Game(Mode):
    def __init__(self, core):
        Mode.__init__(self, core, 50)

        self.map = Map()
        self.map.loadLevel(1)

        self.player = Player((200,200))
        self.hud = HUD(self.player)

        self.bullets = []

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

        #Draw bullets
        for b in self.bullets:
            b.draw(screen, self)

        self.map.drawMobsInView(screen, self)

        self.hud.draw(screen, self)

    def onPreDraw(self, core, numTicks):
        pass

        
    def onComputations(self, core, numTicks):
        states = key.get_pressed()
        mX = 0
        mY = 0

        if states[K_w]:
            #Player move up
            mY = -1
        if states[K_s]:
            #Player move down
            mY = 1
        if states[K_a]:
            #Player move left
            mX = -1
        if states[K_d]:
            #Player move right
            mX = 1

        self.player.move(mX, mY, self.map)

        #Activate mobs / do AI
        self.map.updateMobs(self)

        for b in self.bullets:
            b.move()
            if b.hitWall(self.map):
                self.bullets.remove(b)
                continue

            mobHitted = b.hitMob(self.map)
            if not mobHitted == False:
                self.bullets.remove(b)
                self.map.mobWasHit(mobHitted, self.player.weapons[0]) 
                #Add splash animation?

        self.player.setFacing(mouse.get_pos(), self)

        if mouse.get_pressed()[0]:
            #Fire weapon
            ret = self.player.fireWeapon(numTicks)
            if ret != None:
                self.bullets.append(ret)

    def handleEvent(self, event, core, numTicks):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                core.revertLastMode()
