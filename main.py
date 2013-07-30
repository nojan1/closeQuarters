#!/usr/bin/python2

# Submission for the summer multimedia course project part
# =======================================================
# Game is a 2D top view zombie shooter game in cramped coridors
# It was tested with: python 2.7.5 and pygame 1.9.1 under Arch Linux
#  
# Author: Niklas Hedlund
# Web: https://github.com/nojan1/closeQuarters.git
# License: GPL

# main.py: Startup file for the game, creates core and starts the game loop


from core import Core
from menu import *
        
if __name__ == "__main__":
    #core = Core((800,600), False)
    core = Core((1024,768), False, drawFPS=True)
    core.doInit()
    core.setActiveMode(Menu(core))
    core.enterLoop()
