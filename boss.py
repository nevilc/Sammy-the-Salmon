from __future__ import division

import pygame

from visible import *
from score import *

import vector

class Boss(Visible):
	sprite_path = "gfx/boss.png"
	sprite_res = (137, 291)
	sprite_swim = Subsprite(0, 4)
	sprite_charge = Subsprite(1, 4)
	
	list = []
	
	__dmg_max = 60
	
	__speed = 110
	__charge_speed = 220
	
	__range = 256
	
	score = 5000
	
	__whirlsecs = 2.0
	
	__charge_chance = 0.1
	
	sound_charge = None
	sound_charge_path = "snd/bear.wav"
	
	sound_announce = None
	sound_announce_path = "snd/bear_call.wav"
	
	def __init__(self, pos):
		super(Boss, self).__init__()
		
		self.list.append(self)
		
		self.set_animation(self.sprite_swim, 4)
		
		self.set_position(pos)
		
		self.__dmg = 0
		
		self.target = None
		self.whirl = False
		
		self.idle = 0.0
		
		if not self.sound_charge:
			self.sound_charge = pygame.mixer.Sound(self.sound_charge_path)
		if not self.sound_announce:
			self.sound_announce = pygame.mixer.Sound(self.sound_announce_path)
		
		self.charging = False
		
		self.active = False
		
	def update(self, delta, view):
		super(Boss, self).update(delta)
		
		if self.rect.colliderect(view):
			if not self.active:
				self.active = True
				self.sound_announce.play()
		
			if self.idle > 0:
				self.idle -= delta
			else:
				if self.whirl:
					v = (self.target.centerx - self.rect.centerx, self.target.centery - self.rect.centery)
					mag = vector.mag(v)
					if mag < 300 * delta:
						self.rect.center = self.target.center
						self.whirl = False
						self.target = None
						self.idle = self.__whirlsecs
						self.charging = False
					else:
						v = vector.muls(vector.divs(v, vector.mag(v)), 300 * delta)
						self.move(v)
				else:
					if self.charging:
						self.move((0, self.__charge_speed * delta))
						self.rect.bottom = min(self.rect.bottom, view.bottom)
						if self.rect.bottom == view.bottom:
							self.charging = False
							self.set_animation(self.sprite_swim, 4)
					elif self.target:
						v = (self.target.centerx - self.rect.centerx, self.target.centery - self.rect.centery)
						mag = vector.mag(v)
						if mag < self.__speed * delta:
							self.rect.center = self.target.center
							self.set_animation(self.sprite_swim, 4)
							self.target = None
						else:
							v = vector.muls(vector.divs(v, vector.mag(v)), self.__speed * delta)
							self.move(v)
					else:
						if random.random() < self.__charge_chance:
							self.charging = True
							self.set_animation(self.sprite_charge, 4)
							self.sound_charge.play()
						else:
							self.target = pygame.Rect((self.rect.left + random.randint(-self.__range, self.__range), self.rect.top + random.randint(-self.__range, self.__range)), (137, 274))
							
							self.target.left = max(self.target.left, 144)
							self.target.right = min(self.target.right, 768 - 144)
							self.target.top = max(self.target.top, view.top)
							self.target.bottom = min(self.target.bottom, view.top + (864 * 0.75))
				
		
	def damage(self, amount):
		self.__dmg += amount
		if self.whirl or self.idle > 0:
			self.__dmg += amount
		
		if self.__dmg >= self.__dmg_max:
			if not self.destroy:
				score.add(self.score)
				self.destroy = True
	
	def getDamage(self):
		return (self.__dmg, self.__dmg_max)
		
	def getCharging(self):
		return self.charging