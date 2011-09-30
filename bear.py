from __future__ import division

import pygame
from visible import *

"""
class BearArm(Visible):
	sprite_path = "gfx/bear_arm.png"
	sprite_res = (240, 96)
	sprite_swipe = Subsprite(0, 2)
	
	list = []
	
	def __init__(self, pos):
		super(BearArm, self).__init__()
		
		self.list.append(self)
		
		self.set_animation(self.sprite_swipe, 0.5)
		
		self.set_position(pos)
		
	def attack(self):
		if not self.visible:
			self.visible = True
	
	def update(self, delta, view):
		super(BearArm, self).update(delta)"""
		

class Bear(Visible):
	sprite_path = "gfx/bear.png"
	sprite_res = (274, 137)
	sprite_swipe = Subsprite(0, 4)
	
	list = []
	
	__speed = 360
	__dist = 120
	
	sound_attack = None
	sound_attack_path = "snd/bear.wav"

	def __init__(self, pos):
		super(Bear, self).__init__()
		
		self.list.append(self)
		
		self.set_animation(self.sprite_swipe, 0)
		
		self.set_position(pos)
		
		# reverse image if on the right bank
		if self.rect.left > 144:
			#self.set_scale((-1.0, 1.0))
			self.flip = (True, False)
		else:
			self.rect.left -= 274 - 144
			
		if not self.sound_attack:
			self.sound_attack = pygame.mixer.Sound(self.sound_attack_path)
			
		self.__attacking = False
		
	def update(self, delta, view):
		super(Bear, self).update(delta)
		
		if self.__attacking:
			if self.flip[0]:
				self.move((-self.__speed * delta, 0))
				self.rect.right = max(self.rect.right, view.right - self.__dist)
			else:
				self.move((self.__speed * delta, 0))
				self.rect.left = min(self.rect.left, self.__dist)
		
		
	def attack(self):
		if not self.__attacking:
			self.__attacking = True
			self.set_animation(self.sprite_swipe, 4)
			self.sound_attack.play()
		