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

        for line in open(path, "r"):
            x = []
            for char in line:
                if char == ".":
                    x.append(None)
                elif char == "#":
                    x.append(Floor())
                elif char == "W":
                    x.append(Wall())
                else:
                    print("Warning: Unknown tile; ", char)

            self.tiles.append(x)
            
    def drawTilesInView(self, screen, window):
        

    def get(self, x, y):
        try:
            return self.tiles[x][y]
        except:
            return False
