from __future__ import division

import random

from visible import *

class Log(Visible):
	sprite_path = "gfx/log.png"
	sprite_res = (144, 48)
	sprite_anims = [Subsprite(0, 1), Subsprite(1, 1)]
	
	list = []
	
	__rotation_max = 15.0
	
	__drift_speed = 80
	
	def __init__(self, pos):
		super(Log, self).__init__()
		
		self.list.append(self)
		
		# Choose a rock type at random when created
		self.set_animation(self.sprite_anims[random.randrange(0, self.sprite.get_height() / self.sprite_res[1])], 0)
		
		# Give each log a slight rotation
		self.set_rotation(random.uniform(-self.__rotation_max, self.__rotation_max))
		
		self.set_position(pos)
		
	def update(self, delta, view):
		super(Log, self).update(delta)
		
		# Only drift if on screen
		if self.rect.colliderect(view):
			self.rect.top += self.__drift_speed * delta