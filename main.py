#!/usr/bin/python2

from core import Core
from menu import Menu
        
if __name__ == "__main__":
    core = Core((800,600), False)
    core.doInit()
    core.setActiveMode(Menu(core))
    core.enterLoop()
