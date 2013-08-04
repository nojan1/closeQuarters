# map.py: The Map class represents a instance of a game world, is responsible for parsing level files and creating / containing all the tiles, mobs and such. Also does all the collision calculations
# Author: Niklas Hedlund

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
from levelgen import LevelGenerator

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

        tileTextures = TextureSet("dungeon_crawl.png")
        zombieTextures = TextureSet("zombie_topdown.png")
        spiderTextures = TextureSet("spider_topdown.png")

        mobDict = {"Z": [Zombie, 2, zombieTextures], "S": [Spider, 4, spiderTextures]}

        path = os.path.join(LEVELPATH, str(levelID)+".lvl")
        if os.path.exists(path):
           data = open(path, "r").read()
        else:
            levelGen = LevelGenerator()
            data = levelGen.generateOutput()
            print("Note: Level was auto generated")

        for yPos,line in enumerate(data.split("\n")):
            x = []
            for xPos, char in enumerate(line.strip().upper()):
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
                elif char == "L":
                    x.append( WeaponPickup(pos, tileTextures, WeaponFactory("laser")) )
                elif char == "H":
                    x.append( HealthPickup(pos, tileTextures) )

                #Add mobs map
                elif char in mobDict:
                    #Mobs to allocate later when the tile grid is complete
                    mobsToAlloc.append([pos, mobDict[char][1], mobDict[char][0], mobDict[char][2], ai])
                    
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

    def isAllowedPosition(self, rectToCheck, isPlayer = False):
        tileIndexes = self.getTileIndexes(rectToCheck.center)

        #Limit indexes to avoid out of band errors
        upperY = tileIndexes[1] + 2
        if upperY > len(self.tiles) - 1:
            upperY = len(self.tiles) - 1

        lowerY = tileIndexes[1] - 1
        if lowerY < 0:
            lowerY = 0

        upperX = tileIndexes[0] + 2
        if upperX > len(self.tiles[ upperY ]) - 1:
            upperX = len(self.tiles[ upperY ]) - 1
            
        lowerX = tileIndexes[0] - 1
        if lowerX < 0:
            lowerX = 0
  
        for y in range(lowerY, upperY):
            for tile in self.tiles[y][lowerX: upperX]:
                if tile != None and tile.getRect().colliderect(rectToCheck):
                    if tile.onCollision(self.game, isPlayer):
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
        for (tileCoords, numMobs, mobClass, mobTextures, ai) in mobsToAlloc: 
            basePos = (tileCoords[0] * TILESIZE[0], tileCoords[1] * TILESIZE[1])

            posDirs = [(0,-1), (1,0), (0,1), (-1,0)]
            random.shuffle(posDirs)

            for i in range(numMobs):
                testMob = mobClass(basePos, ai, mobTextures)
                if self.mobPresent(testMob.getRect()):
                    #Find new position
                    addedDistance = 0
                    while 1:
                        addedDistance += testMob.getRect().width
                        newPos = (basePos[0] + (posDirs[0][0] * addedDistance), basePos[1] + (posDirs[0][1] * addedDistance))
                        testMob = mobClass(newPos, ai, mobTextures)
                
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
