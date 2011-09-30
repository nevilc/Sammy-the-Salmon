from __future__ import division

import pygame

import vector

from visible import *
from score import *

class Fish(Visible):
	sprite_path = "gfx/fish.png"
	sprite_res = (36, 53)
	sprite_idle = Subsprite(0, 2)
	
	list = []
	
	__drift_speed = 160
	
	__dmg_max = 3

	__points = 10
	__slope = 0.0
	__velocity = (0, __drift_speed)
	
	#determines rate of motion toward whirlpool, higher numbers move slower
	__whirl_rate = 10
	
	score = 50
	
	def __init__(self, pos):
		super(Fish, self).__init__()
		
		self.list.append(self)
		
		self.set_animation(self.sprite_idle, 5)
		
		self.set_position(pos)
		
		self.__dmg = 0
		self.target = None
		
		#switch if hit by the whirlpool to set target priority
		self.whirl = False
		
		
	def update(self, delta, view):
		super(Fish, self).update(delta)
		
		# Only drift if on screen
		#if self.rect.colliderect(view):
		#	self.rect.top += self.__drift_speed * delta
		
		#if whirlpool hits do not allow fish to target salmon
		if self.target == None:
			self.move((0, self.__drift_speed * delta))
		else:
			if not self.whirl:
				self.move((self.__velocity[0] * delta, self.__velocity[1] * delta ))
			else:
				v = (self.target.centerx - self.rect.centerx, self.target.centery - self.rect.centery)
				mag = vector.mag(v)
				if mag < 300 * delta:
					self.rect.center = self.target.center
				else:
					v = vector.muls(vector.divs(v, vector.mag(v)), 300 * delta)
					self.move(v)
			
	def damage(self, amount):
		self.__dmg += amount
		if self.__dmg >= self.__dmg_max:
			if not self.destroy:
				self.destroy = True
				score.add(self.score)
			# DeadFish(self.rect.topleft)
			