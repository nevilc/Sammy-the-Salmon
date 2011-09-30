from __future__ import division

import random

from visible import *

class Rock(Visible):
	sprite_path = "gfx/rock.png"
	sprite_res = (48, 48)
	sprite_anims = [Subsprite(0, 1), Subsprite(1, 1)]
	
	list = []
	
	def __init__(self, pos):
		super(Rock, self).__init__()
		
		self.list.append(self)
		
		# Choose a rock type at random when created
		self.set_animation(self.sprite_anims[random.randrange(0, self.sprite.get_height() / self.sprite_res[1])], 0)
		
		# Rotate each rock randomly
		self.set_rotation(random.uniform(0, 360))
		
		self.set_position(pos)
	
	def update(self, delta, view):
		super(Rock, self).update(delta)
		
		