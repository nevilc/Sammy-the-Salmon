from __future__ import division

import pygame
import random

from visible import *

# Move this somewhere else eventually
def sign(i):
	if i > 0:
		return 1
	elif i < 0:
		return -1
	else:
		return 0

class EagleSpawner(object):
	list = []

	sound_caw_path = "snd/eagle_caw.wav"
	sound_caw = None

	#delay before eagle spawns in seconds
	__delay = 2.0

	def __init__(self, pos):
		self.list.append(self)
		
		self.rect = pygame.Rect(pos, (1, 1))
		
		self.timer = 0.0
		
		self.active = False
		self.destroy = False
		
		if not self.sound_caw:
			self.sound_caw = pygame.mixer.Sound(self.sound_caw_path)
		
	def update(self, delta, view):
		if not self.active and self.rect.colliderect(view):
			self.active = True
			self.sound_caw.play()
		if self.active and self.timer < self.__delay:
			self.timer += delta
			if self.timer >= self.__delay:
				Eagle((self.rect.left, view.top - 96))
				self.destroy = True
	
	def draw(self, target, view):
		pass

class Eagle(Visible):
	sprite_path = "gfx/eagle.png"
	sprite_res = (240, 114)
	sprite_idle = Subsprite(0, 1)
	
	
	sound_flap_path = "snd/eagle_flap.wav"
	sound_flap = None
	
	list = []
	
	# How many pixels before going on screen the eagle will caw and activate
	__prewarning = 200 * 2.0
	
	# How high up the eagle starts
	__z_initial = 480
	
	# How low the eagle must be before it can damage the salmon
	__z_threshold = 48
	
	# The scale of the eagle at its highest and lowest
	__scale_max = 2.0
	__scale_min = 1.0
	
	# Z coordinate speeds in pixels per second
	__drop_speed = 200
	__rise_speed = 100
	
	# Vertical move speed limits
	__y_min_speed = 30 * 1.25
	__y_max_speed = 120 * 1.5
	# Horizontal move speed limits
	#__x_min_speed = 20
	#__x_max_speed = 100
	__x_min_speed = 0
	__x_max_speed = 0
	
	def __init__(self, pos):
		super(Eagle, self).__init__()
		
		self.list.append(self)
		
		self.set_animation(self.sprite_idle, 0)
		
		self.set_position(pos)
	
		#self.visible = False
		
		# Position in the third dimension
		# Affects scaling and collision with salmon
		self.z = self.__z_initial
		
		# Eagle starts inactive until close to the view
		#self.active = False
		# Has the eagle begun to rise after attacking
		self.rising = False
		
		# The targeted location (i.e., Salmon's rect), Game should update this
		self.target = None
		
		if not self.sound_flap:
			self.sound_flap = pygame.mixer.Sound(self.sound_flap_path)
		
	def update(self, delta, view):
		super(Eagle, self).update(delta)
		
		#if self.active:
		if self.rect.colliderect(view):
			if self.rising:
				self.z += self.__rise_speed * delta
			else:
				self.z = max(0, self.z - self.__drop_speed * delta)
				if self.z == 0:
					self.rising = True
			
			if self.target and not self.rising:
				#self.rect.centery += max(self.__y_min_speed, min(self.__y_max_speed, (self.target.top - self.rect.centery) / (self.z / self.__drop_speed))) * delta
				
				# Pygame rects can only store intergers! This is bad for slow movement!
				# Since this will usually be slower than 1px/sec, move whole
				# pixels based on probability
				#xdelta = max(self.__x_min_speed, min(self.__x_max_speed, abs(self.target.centerx - self.rect.centerx) / (self.z / self.__drop_speed))) * delta
				#sgn = sign(self.target.centerx - self.rect.centerx)
				#self.rect.centerx += sgn * math.floor(xdelta)
				#if random.random() < xdelta:
				#	self.rect.centerx += sgn
				self.move((max(self.__x_min_speed, min(self.__x_max_speed, abs(self.target.centerx - self.rect.centerx) / (self.z / self.__drop_speed))) * delta, max(self.__y_min_speed, min(self.__y_max_speed, (self.target.top - self.rect.centery) / (self.z / self.__drop_speed))) * delta))
			else:
				self.move((0, (self.__y_min_speed + self.__y_max_speed) / 2 * delta))
			
			# Set the scale of the sprite based on the height
			self.set_scale((self.__scale_min + (self.__scale_max - self.__scale_min) * (self.z / self.__z_initial), self.__scale_min + (self.__scale_max - self.__scale_min) * (self.z / self.__z_initial)))
				
		#else:
		#	if self.rect.move(0, self.__prewarning).colliderect(view):
		#		self.sound_caw.play()
		#		self.active = True
		#		self.visible = True
		
	def is_attacking(self):
		return self.z <= self.__z_threshold