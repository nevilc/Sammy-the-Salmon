from __future__ import division

import pygame
import math

import vector
from visible import *

class Bubble(Visible):
	sprite_path = "gfx/bubble.png"
	sprite_res = (24, 24)
	sprite_tiny = Subsprite(0, 1)
	
	list = []
	
	__speed_base = 300
	#__speed_base = 60
	
	def __init__(self, pos, velocity, dir):
		super(Bubble, self).__init__()
		
		self.list.append(self)
		
		self.set_animation(self.sprite_tiny, 0)
		
		#self.set_position(pos)
		self.rect.center = pos
		self.__velocity = velocity
		self.__direction = dir
		
		self.set_rotation(random.uniform(0, 360))
	
	def update(self, delta, view):
		super(Bubble, self).update(delta)
		
		self.move(vector.muls(self.__velocity, delta))
		self.move((self.__speed_base * math.cos(self.__direction) * delta, self.__speed_base * math.sin(self.__direction) * delta))
		
		#self.move((self.__velocity[0] * delta, self.__velocity[1] * delta))
		#self.move((self.__speed * delta * math.cos(math.radians(self.__dir)), self.__speed * delta * math.sin(math.radians(self.__dir))))
		
		# Destroy bubbles once they are outside of view
		if not self.is_in(view):
			self.destroy = True
					