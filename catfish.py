from __future__ import division

import pygame

import vector
from visible import *
from score import *

class Catfish(Visible):
	sprite_path = "gfx/catfish.png"
	sprite_res = (64, 84)
	sprite_idle = Subsprite(0, 8)
	
	list = []
	
	__dmg_max = 5
	
	__chase_speed = 40
	
	__drift_speed = 40
	
	__velocity = (0, __drift_speed)
	
	score = 200
	
	def __init__(self, pos):
		super(Catfish, self).__init__()
		
		self.list.append(self)
		
		self.set_animation(self.sprite_idle, 10)
		
		self.set_position(pos)
		
		self.__dmg = 0
		
		self.bound = None
		self.target = None
		self.whirl = False
		
	def update(self, delta, view):
		super(Catfish, self).update(delta)
		
		if self.rect.colliderect(view):
			if self.whirl:
				v = (self.target.centerx - self.rect.centerx, self.target.centery - self.rect.centery)
				mag = vector.mag(v)
				if mag < 300 * delta:
					self.rect.center = self.target.center
				else:
					v = vector.muls(vector.divs(v, vector.mag(v)), 300 * delta)
					self.move(v)
			else:
				if self.bound.colliderect(self.target):
					if self.rect.centerx < self.target.centerx:
						self.move((self.__chase_speed * delta, 0))
						self.rect.centerx = min(self.rect.centerx, self.target.centerx)
						self.rect.right = min(self.rect.right, self.bound.right)
					elif self.rect.centerx > self.target.centerx:
						self.move((-self.__chase_speed * delta, 0))
						self.rect.centerx = max(self.rect.centerx, self.target.centerx)
						self.rect.left = max(self.rect.left, self.bound.left)
					
				self.move(vector.muls(self.__velocity, delta))
		
	def damage(self, amount):
		self.__dmg += amount
		if self.__dmg >= self.__dmg_max:
			if not self.destroy:
				self.destroy = True
				score.add(self.score)
	
	
