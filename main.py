from __future__ import division

import sys
import pygame
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

from game import *

while True:
	game = Game()

	while game.update() != -1:
		#game.update()
		game.draw()
		
	del game