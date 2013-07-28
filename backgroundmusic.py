# backgroundmusic.py: Handles the in game background music, uses a simple form of random playlist
# Author: Niklas Hedlund

from config import*
from pygame import *
import os
import random

class BackgroundMusic(object):
    def __init__(self):
        #Load all the filenames from music folder
        self.files = []
        for f in os.listdir(MUSICPATH):
            if f != "." and f != "..":
                self.files.append(f)

        #Pygame event system will be used to trigger new track
        mixer.music.set_endevent(USEREVENT)

    def playTrack(self):
        audioFile = self.files[ random.randint(0, len(self.files)-1) ]
        mixer.music.load(os.path.join(MUSICPATH, audioFile))
        mixer.music.play()

    def stop(self):
        mixer.music.stop()

    def pause(self):
        mixer.music.pause()

    def unpause(self):
        mixer.music.unpause()
