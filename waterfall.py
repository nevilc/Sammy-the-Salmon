import pygame

from visible import *

class Waterfall(Visible):
	sprite_path = "gfx/waterfall.png"
	sprite_res = (480, 240)
	sprite_idle = Subsprite(0, 2)
	
	list = []
	
	sound_waterfall = None
	sound_waterfall_path = "snd/waterfall.wav"
	
	def __init__(self, pos):
		super(Waterfall, self).__init__()
		
		self.list.append(self)
		
		self.set_animation(self.sprite_idle, 6)
		
		self.set_position(pos)
		
		if not self.sound_waterfall:
			self.sound_waterfall = pygame.mixer.Sound(self.sound_waterfall_path)
		
		self.active = False
		
	def update(self, delta, view):
		super(Waterfall, self).update(delta)
		
		if self.rect.colliderect(view):
			if not self.active:
				self.active = True
				self.sound_waterfall.play(-1)
