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
        
import argparse

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='2D top view zombie shooter game in cramped coridors', epilog='Have fun shooting zombies :)')
    parser.add_argument("--draw-fps", help="Display FPS counter in upper left corner", action="store_true")
    parser.add_argument("-r", "--resolution", help="The size of game window to use. Warning changing this will break the layout of the menu and dialogs", default="1024x768")
    parser.add_argument("-f", "--fullscreen", help="Run in fullscreen", action="store_true")
    args = parser.parse_args()

    if "x" in args.resolution:
        res = tuple( [int(x) for x in args.resolution.split("x")] )
    else:
        print("Warning: Unsupported resolution format defaulting to 1024x768")
        res = (1024, 768)

    core = Core(res, args.fullscreen, args.draw_fps)
    core.doInit()
    core.setActiveMode(Menu(core))
    core.enterLoop()
