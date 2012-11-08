from __future__ import division

import pygame
import sys

from rock import *
from log import *
from bear import *
from eagle import *
from waterfall import *
from boss import *


class Map(object):

	blocksize = 24
	
	color_water = pygame.Color(0, 174, 239, 255)
	color_rock 	= pygame.Color(142, 142, 142, 255)
	color_log 	= pygame.Color(85, 60, 30, 255)
	color_grass = pygame.Color(12, 255, 0, 255)
	color_bear 	= pygame.Color(0, 0, 0, 255)
	color_eagle = pygame.Color(255, 255, 255, 255)
	color_boss  = pygame.Color(255, 0, 0, 255)
	
	def __init__(self, file, ll):
		"""Creates map from image file"""
		self.image = pygame.image.load(file)
		
		self.levels_left = ll
		
		#self.data = [line.rstrip() for line in self.data]
		
		# Objects will take care of the sprites themselves
		#self.rock = pygame.image.load("rock.png").convert()
		#self.log = pygame.image.load("log.png").convert()
		
		# No boundary art yet
		#self.boundary = pygame.image.load("boundary.png").convert()
		
		# How fast the river moves in pixels per second
		#self.riverspeed = 192
		
		# Hardcoding, yay!
		#if file == "level/03.png":
		#	Boss((400, 400))
		#else:
		#	Waterfall((144, 0))
		
		self.create()
			
	def create(self):
		"""Draw the map to the screen"""
		
		self.width = self.image.get_width() * self.blocksize
		self.height = self.image.get_height() * self.blocksize
		
		if self.levels_left > 0:
			Waterfall((144, 0))
		else:
			Boss((400, 400))
			
		for j in range(0, self.image.get_height()):
			for i in range(0, self.image.get_width()):
				color = self.image.get_at((i, j))
				location = (i * self.blocksize, j * self.blocksize)
				
				#Determine size of each object in scaled down pixel size to avoid painting
				#duplicate overlapping objects.
				if color == self.color_rock:
					Rock(location)
					
					# Set 2x2 area to water color so multiple rocks aren't created
					# TODO Put this is a for loop eventually
					self.image.set_at((i + 1, j), self.color_water)
					self.image.set_at((i, j + 1), self.color_water)
					self.image.set_at((i + 1, j + 1), self.color_water)
					
					#print("Rock")
				elif color == self.color_log:
					Log(location)
					
					# Set 5x2 area to water color
					self.image.set_at((i + 1, j), self.color_water)
					self.image.set_at((i + 2, j), self.color_water)
					self.image.set_at((i + 3, j), self.color_water)
					self.image.set_at((i + 4, j), self.color_water)
					self.image.set_at((i + 5, j), self.color_water)
					self.image.set_at((i, j + 1), self.color_water)
					self.image.set_at((i + 1, j + 1), self.color_water)
					self.image.set_at((i + 2, j + 1), self.color_water)
					self.image.set_at((i + 3, j + 1), self.color_water)
					self.image.set_at((i + 4, j + 1), self.color_water)
					self.image.set_at((i + 5, j + 1), self.color_water)
					
					#print("Log")
				elif color == self.color_bear:
					Bear(location)
				elif color == self.color_eagle:
					EagleSpawner(location)
				elif color == self.color_grass:
					#print("Grass")
					pass
				elif color == self.color_boss:
					Boss(location)
				else:
					pass
	