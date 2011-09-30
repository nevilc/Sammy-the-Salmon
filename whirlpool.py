import pygame
import sys
import math
import vector

from visible import *
from whitbox import *

class Whirlpool(Visible):
	
	sprite_path = "gfx/whirlpool.png"
	sprite_res = (144, 144)
	sprite_ani = Subsprite(0, 10)
	
	__speed = 400
	__distance = 350
	
	__life_max = 3.0
	
	sound_whirl = None
	sound_whirl_path = "snd/whirlpool.wav"
	
	list = []
	
	def __init__(self, pos, vel, dir):
		"""Initialize a whirlpool"""
		super(Whirlpool, self).__init__()
		
		self.list.append(self)
		#self.set_position(pos)
		self.rect.center = pos
		self.__velocity = vel
		self.__direction = dir
		self.__created_hitbox = False
		self.__windup = True
		
		self.__traveled = 0.0
		self.__time_alive = 0.0
		
		if not self.sound_whirl:
			self.sound_whirl = pygame.mixer.Sound(self.sound_whirl_path)
		self.sound_whirl.play()
		
		self.set_animation(self.sprite_ani, 4)
		
	def update(self, delta, view):
		super(Whirlpool, self).update(delta)
		if not self.__windup:
			if self.__traveled < self.__distance:
				self.move(vector.muls(self.__velocity, delta))
				self.move((self.__speed * delta * math.cos(self.__direction), self.__speed * delta * math.sin(self.__direction)))
				self.__traveled += self.__speed * delta
			elif self.__created_hitbox == False:
				WHitbox((self.rect.topleft[0] - self.rect.w, self.rect.topleft[1] - self.rect.h))
				self.__created_hitbox = True
			else:
				self.__time_alive += delta
		
		if self.__time_alive >= self.__life_max:
			self.destroy = True
			if WHitbox.list:
				for wh in WHitbox.list:
					wh.destroy = True
			
		#if self.rect.topleft[1] >= view.bottom:
		#	self.destroy = True
		
		self.rect.top = max(self.rect.top, view.top)
		self.rect.left = max(self.rect.left, 144)
		self.rect.right = min(self.rect.right, view.right - 144)
		
	def active(self):
		return self.__traveled >= self.__distance
	
	def set_velocity(self, vel):
		self.__velocity = vel
		
	def set_windup(self, bool):
		self.__windup = bool
	