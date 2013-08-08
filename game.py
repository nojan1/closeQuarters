# game.py: The actual game engine, inherits Mode
# Author: Niklas Hedlund

from pygame import *
import os
import random

from backgroundmusic import *
from mode import Mode
from map import Map
from player import Player
from hud import *
from gameover import GameOverScreen
from splatter import *
from textureset import *

class Game(Mode):
    def __init__(self, core):
        Mode.__init__(self, core, 50)

        #Create player and HUD objects (HUD needs player reference to display health)
        self.player = Player((200,200))
        self.hud = HUD(self.player)

        #Start background music
        self.music = BackgroundMusic()
        self.music.playTrack()

        #Setup and start the map / level sub system
        self.maps = []
        self.activeMap = None
        self.changeMap(0)

        #Load and setup game sound resources
        self.zombiePain = mixer.Sound(os.path.join(SOUNDPATH, "zombie_pain.wav"))
        self.playerHitSounds = [ mixer.Sound(os.path.join(SOUNDPATH, "punch.wav")), mixer.Sound(os.path.join(SOUNDPATH, "bite.wav")) ]
        self.footsteps = mixer.Sound(os.path.join(SOUNDPATH, "footsteps.wav"))
        self.footsteps.set_volume(0.6)
        self.footstepsPlaying = False

        self.bullets = []
        self.splatters = []
        self.splatterTextures = TextureSet("sparks.png")

        #Statistic purposes
        self.shotsFired = 0
        self.shotsHit = 0

    def getMap(self):
        return self.maps[self.activeMap]

    def changeMap(self, newMapID):
        if newMapID < 0:
            print("Error: Level below zero is undefined!")
            return

        #If the requested map is not yet loaded then load it
        if newMapID > len(self.maps) - 1:
            self.maps.append( Map(newMapID, self) )

        #If there already is a active map then we need to save the player pos, before we change to the new one
        if self.activeMap != None:
            self.maps[self.activeMap].playerPosCache = self.player.pos

        print("Got map change request, new ID=%i" % newMapID)
        self.activeMap = newMapID

        #Position for the player is stored in the Map object
        self.player.pos = self.getMap().playerPosCache

    #Return a Rect object of the current displayed (on the monitor) area
    def getView(self):
        tmp = Rect((0, 0), tuple(self.core.res))
        #Center around player
        tmp.center = self.player.pos

        if tmp.x < 0:
            tmp.x = 0

        if tmp.y < 0:
            tmp.y = 0
        
        return tmp

    def onDraw(self, screen, core, numTicks):
        screen.fill((0,0,0))

        self.getMap().drawTilesInView(screen, self)
        self.player.draw(screen, self, numTicks)

        #Draw bullets
        for b in self.bullets:
            b.draw(screen, self)

        self.getMap().drawMobsInView(screen, self, numTicks)

        #Draw blood splatters
        for s in self.splatters:
            s.draw(screen, self, numTicks)

        self.hud.draw(screen, self)

    def onPreDraw(self, core, numTicks):
        pass

    def handlePlayerDamage(self, damage):
        #Play random player hit sound and make the player hurt
        self.playerHitSounds[ random.randint(0,len(self.playerHitSounds)-1) ].play()
        self.player.takeDamage(damage)

        if self.player.health == 0:
            #Gameover
            self.footsteps.stop()
            self.music.stop()
            self.core.setActiveMode( GameOverScreen(self) )
        
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

        if mX == 0 and mY == 0:
            #If the player didn't move we stop the footsteps
            self.footsteps.stop()
            self.footstepsPlaying = False
        else:
            if not self.footstepsPlaying:
                self.footsteps.play()
                self.footstepsPlaying = True

        self.player.move(mX, mY, self.getMap())

        #Activate mobs / do AI
        self.getMap().updateMobs(self, numTicks)

        #Check for dead splatters
        for s in self.splatters:
            if s.isDead():
                self.splatters.remove(s)

        for b in self.bullets:
            b.move()
            #Handle bullet collision with wall
            if b.hitWall(self.getMap()):
                self.bullets.remove(b)
                continue

            #Check if the bullet hit a Mob
            mobHitted = b.hitMob(self.getMap())
            if not mobHitted == False:
                self.shotsHit += 1
                self.bullets.remove(b)
                self.zombiePain.play()
                self.getMap().mobWasHit(mobHitted, self.player.weapons[0]) 
                
                #Add splash animation
                self.splatters.append( Splatter(mobHitted.pos, self.splatterTextures) )

        #Update player facing angle from the mouse position
        self.player.setFacing(mouse.get_pos(), self)

        if mouse.get_pressed()[0]:
            #Fire weapon
            ret = self.player.fireWeapon(numTicks)
            if ret != None:
                self.shotsFired += 1
                self.bullets.append(ret)

        #Used to update the temperature indication on the laser gun
        self.player.weapons[0].weaponUpkeep(numTicks)

    def onSwitchIn(self, core):
        #The background music needs to be restored when the game mode is reloaded
        self.music.unpause()

    def handleEvent(self, event, core, numTicks):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                #Back to menu
                self.music.pause()
                core.revertLastMode()
        elif event.type == USEREVENT:
            #Background music track ended
            self.music.playTrack()
