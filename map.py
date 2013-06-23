import os

from tile import *
from config import *

class Map(object):
    def __init__(self):
        self.tiles = None

    def loadLevel(self, levelID):
        self.tiles = []
        
        path = os.path.join(LEVELPATH, str(levelID)+".lvl")
        if not os.path.exists(path):
            raise Exception("No such levelfile;", path)

        for yPos,line in enumerate(open(path, "r")):
            x = []
            for xPos, char in enumerate(line.strip()):
                pos = (xPos, yPos)
                if char == ".":
                    x.append(None)
                elif char == "#":
                    x.append(Floor(pos))
                elif char == "W":
                    x.append(Wall(pos))
                else:
                    print("Warning: Unknown tile; ", char)

            self.tiles.append(x)
            
    def drawTilesInView(self, screen, game):
        for y in self.tiles:
            for tile in y:
                if tile != None and tile.getRect().colliderect(game.getView()):
                    tile.draw(screen, game)

    def isAllowedPosition(self, rectToCheck):
        for y in self.tiles:
            for tile in y:
                if tile != None and tile.getRect().colliderect(rectToCheck):
                    if tile.onCollision():
                        return False

        return True

    def get(self, x, y):
        try:
            return self.tiles[x][y]
        except:
            return False
