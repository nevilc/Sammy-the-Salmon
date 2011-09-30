from __future__ import division

import pygame
import math
import random

from subsprite import *

class Visible(object):
	
	# Static sprite variables, copy these and define for each derived class
	
	#sprite_path = "gfx/name.png"
	#sprite_res = (width, height)
	#sprite_idle = subsprite(row, columns)
	
	sprite_path = None
	sprite = None
	sprite_res = None
	sprite_idle = None
	
	def __init__(self):
		# Derived class checklist:
		#	super(ClassName, self).__init__()
		#	self.set_animation(animation, animspeed, frame)
		
		if self.sprite == None:
			self.sprite = pygame.image.load(self.sprite_path).convert_alpha()
		
		# Sprite position
		self.rect = pygame.Rect((0, 0), (0, 0))
		self.set_position((0, 0))
		# Sprite scaling tuple
		self.set_scale((1.0, 1.0))
		# Sprite rotation in degrees (CCW)
		self.set_rotation(0.0)
		
		# If set to false, draw() will be skipped
		self.visible = True
		
		# If set to True, will be pruned from the list at the end of the frame
		self.destroy = False
		
		self.flip = (False, False)
		
	def update(self, delta):
		# Derived class checklist:
		#	super(ClassName, self).update(delta)
		self.frame += delta * self.__animspeed
		
	def draw(self, target, view):
		# Only draw the sprite if it is on the screen
		if self.visible and view.colliderect(self.rect):
			# Create a subsurface of the selected frame from the sprite sheet
			subspr = self.sprite.subsurface((((math.floor(self.frame) % self.__animation.frames) * self.sprite_res[0], self.__animation.position * self.sprite_res[1]), self.sprite_res))
			
			if self.flip[0] or self.flip[1]:
				subspr = pygame.transform.flip(subspr, self.flip[0], self.flip[1])
			
			# Scale and rotate the surface if necessary
			#if self.__scale != (1, 1) or self.__rotation != 0:
			if self.__scale != (1.0, 1.0):
				subspr = pygame.transform.scale(subspr,(int(self.sprite_res[0] * self.__scale[0]), int(self.sprite_res[1] * self.__scale[1])))
			if self.__rotation != 0.0:
				subspr = pygame.transform.rotozoom(subspr, self.__rotation, 1.0)
			target.blit(subspr, (self.rect.left - view.left, self.rect.top - view.top), subspr.get_rect())
	
	def set_position(self, position):
		self.rect.topleft = position

	def move(self, distance):
		if random.random() < abs(math.fmod(distance[0], 1)):
			if distance[0] > 0:
				self.rect.centerx += 1
			else:
				self.rect.centerx -= 1
		if random.random() < abs(math.fmod(distance[1], 1)):
			if distance[1] > 0:
				self.rect.centery += 1
			else:
				self.rect.centery -= 1
		#self.rect = pygame.Rect((self.rect[0] + distance[0], self.rect[1] + distance[1]), self.rect.size)
		self.rect.centerx += distance[0]
		self.rect.centery += distance[1]
	
	def set_animation(self, animation, animspeed, frame = 0):
		# Current animation (idle, attacking, etc.) of the sprite, specified by subsprite object
		self.__animation = animation
		# Current animation frame (horizontal position on spritesheet)
		self.__animspeed = animspeed
		# Animation speed, measured in frames per second
		self.frame = frame
	
	def set_scale(self, scale):
		c = self.rect.center
		self.__scale = scale
		self.rect.size = (self.sprite_res[0] * scale[0], self.sprite_res[1] * scale[1])
		self.rect.center = c
		
	def get_scale(self):
		return self.__scale
		
	def set_rotation(self, rotation):
		self.__rotation = rotation
		
	def get_rotation(self):
		return self.__rotation
		
	def rotate(self, degrees):
		self.__rotation += degrees
		
	def is_in(self, area):
		return self.rect.colliderect(area)
	