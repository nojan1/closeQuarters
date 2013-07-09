import os
import random
import math

from tile import *
from config import *
from zombie import *
from spider import *
from textureset import *
from ai import AI
from pickup import *
from weapon import WeaponFactory

class Map(object):
    def __init__(self, levelID, game):
        self.tiles = None
        self.mobs = []

        self.game = game
        self.playerPosCache = None
        
        self.levelID = levelID
        self.loadLevel(levelID)

    def loadLevel(self, levelID):
        ai = AI()
        self.tiles = []
        mobsToAlloc = []

        mobDict = {"Z": [Zombie, 1], "S": [Spider, 1]}

        tileTextures = TextureSet("tiles.png")

        path = os.path.join(LEVELPATH, str(levelID)+".lvl")
        if not os.path.exists(path):
            raise Exception("No such levelfile;", path)

        for yPos,line in enumerate(open(path, "r")):
            x = []
            for xPos, char in enumerate(line.strip()):
                pos = (xPos, yPos)
                if char == "." or char == " ":
                    x.append(Empty(pos, tileTextures))
                elif char == "#":
                    x.append(Floor(pos, tileTextures))
                elif char == "W":
                    x.append(Wall(pos, tileTextures))

                #Store this position as the player saved position
                elif char == "P":
                    self.playerPosCache = (xPos * TILESIZE[0], yPos * TILESIZE[1])

                    #Fill in blank with floor
                    x.append(Floor(pos, tileTextures))

                #Handle level change
                elif char == "+":
                    x.append( MapChange(pos, tileTextures, levelID + 1) )
                elif char == "-":
                    x.append( MapChange(pos, tileTextures, levelID - 1) )
                             
                #Add pickups
                elif char == "R":
                    x.append( WeaponPickup(pos, tileTextures, WeaponFactory("autorifle")) )

                #Add mobs map
                elif char in mobDict:
                    #Mobs to allocate later when the tile grid is complete
                    mobsToAlloc.append([pos, mobDict[char][1], mobDict[char][0], ai])
                    
                    #Fill in blank with floor
                    x.append(Floor(pos, tileTextures))
                else:
                    print("Warning: Unknown tile; ", char)

            self.tiles.append(x)

        self.allocateMobs(mobsToAlloc)
            
    def updateMobs(self, game, tickCount):
        for m in self.mobs:
            #if m.getRect().colliderect(game.getView()):
            m.onActivation(game, tickCount)

    def drawMobsInView(self, screen, game, numTicks):
        for m in self.mobs:
            if m.getRect().colliderect(game.getView()):
                m.draw(screen, game, numTicks)

    def drawTilesInView(self, screen, game):
        window = game.getView()
        low = self.getTileIndexes(window.topleft)
        
        upperX = (window.width / TILESIZE[0]) + 2 + low[0]
        upperY = (window.height / TILESIZE[1]) + 2 + low[1]

        #Use array slicing to avoid exesive looping
        for y in self.tiles[low[1]:upperY]:
            for tile in y[low[0]:upperX]:
                if tile != None and tile.getRect().colliderect(game.getView()): # <= This might be redundant
                    tile.draw(screen, game)

    def isAllowedPosition(self, rectToCheck):
        tileIndexes = self.getTileIndexes(rectToCheck.topleft)
        
        for y in range(tileIndexes[1] - 1, tileIndexes[1] + 2):
            for tile in self.tiles[y][tileIndexes[0] - 1: tileIndexes[0] + 2]:
                if tile != None and tile.getRect().colliderect(rectToCheck):
                    if tile.onCollision(self.game):
                        return False

        return True

    def getTileFromPos(self, pos):
        x, y = self.getTileIndexes(pos)
        return self.get(x, y)

    def getTileIndexes(self, pos):
        x = int(float(pos[0]) / float(TILESIZE[0]))
        y = int(float(pos[1]) / float(TILESIZE[1]))
        
        return (x,y)

    def mobWasHit(self, mobHitted, weapon):
        if mobHitted.takeDamage(weapon.damage):
            self.mobs.remove(mobHitted)

    def mobPresent(self, rect):
        for m in self.mobs:
            if m.getRect().colliderect(rect):
                return True
        
        return False

    def allocateMobs(self, mobsToAlloc):
        for (tileCoords, numMobs, mobClass, ai) in mobsToAlloc: 
            basePos = (tileCoords[0] * TILESIZE[0], tileCoords[1] * TILESIZE[1])

            posDirs = [(0,-1), (1,0), (0,1), (-1,0)]
            random.shuffle(posDirs)

            for i in range(numMobs):
                testMob = mobClass(basePos, ai)
                if self.mobPresent(testMob.getRect()):
                    #Find new position
                    addedDistance = 0
                    while 1:
                        addedDistance += testMob.getRect().width
                        newPos = (basePos[0] + (posDirs[0][0] * addedDistance), basePos[1] + (posDirs[0][1] * addedDistance))
                        testMob = mobClass(newPos, ai)
                
                        if not self.isAllowedPosition(testMob.getRect()):
                            posDirs.pop(0)
                            addedDistance = 0
                            if len(posDirs) == 0:
                                print("Warning unable to place mob num %i with base position; x=%i and y=%i" % (i, basePos))
                                break
                            
                            continue

                        if not self.mobPresent(testMob.getRect()):
                            break

                self.mobs.append(testMob)
                

    def get(self, x, y):
        try:
            return self.tiles[y][x]
        except:
            return False
