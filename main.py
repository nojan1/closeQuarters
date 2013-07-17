#!/usr/bin/python2

from core import Core
from menu import *
        
if __name__ == "__main__":
    #core = Core((800,600), False)
    core = Core((1024,768), False, drawFPS=True)
    core.doInit()
    core.setActiveMode(Menu(core))
    core.enterLoop()
