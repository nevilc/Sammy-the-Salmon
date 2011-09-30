import pygame
import sys

from visible import *

class WHitbox(Visible):
	sprite_path = "gfx/whitbox.png"
	sprite_res = (384, 384)
	sprite_solid = Subsprite(0, 1)
	
	list = []
	
	def __init__(self, pos):
		"""Create area of effect hitbox"""
		super(WHitbox, self).__init__()
		
		self.set_animation(self.sprite_solid, 0)
		self.list.append(self)
		self.set_position(pos)
		
		self.visible = False
		
		
		
	def update(self, delta, view):
		super(WHitbox, self).update(delta)
		
		if self.rect.topleft[1] >= view.bottom:
			self.destroy = True
			
