import os
import random
import math

from tile import *
from config import *
from zombie import *
from textureset import *
from ai import AI

class Map(object):
    def __init__(self):
        self.tiles = None
        self.mobs = []

    def loadLevel(self, levelID):
        ai = AI()
        self.tiles = []
        mobsToAlloc = []

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
                elif char == "Z":
                    #Mobs to allocate later when the tile grid is complete
                    mobsToAlloc.append([pos, 1, Zombie, ai])
                    
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

    def drawMobsInView(self, screen, game):
        for m in self.mobs:
            if m.getRect().colliderect(game.getView()):
                m.draw(screen, game)

    def drawTilesInView(self, screen, game):
        window = game.getView()
        low = self.getTileCoords(window.topleft)
        
        upperX = (window.width / TILESIZE[0]) + 2 + low[0]
        upperY = (window.height / TILESIZE[1]) + 2 + low[1]

        for y in self.tiles[low[1]:upperY]:
            for tile in y[low[0]:upperX]:
                if tile != None and tile.getRect().colliderect(game.getView()): # <= This might be redundant
                    tile.draw(screen, game)

    def isAllowedPosition(self, rectToCheck):
        tile = self.getTileFromPos(rectToCheck.center)
        if tile:
            return not tile.onCollision()
        else:
            return False

    def getTileFromPos(self, pos):
        x, y = self.getTileCoords(pos)
        return self.get(x, y)

    def getTileCoords(self, pos):
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
