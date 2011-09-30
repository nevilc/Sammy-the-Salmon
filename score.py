from __future__ import division

import pygame

class Score:
	__time_baseline = 120 * 1000

	__ms_per_point = 10
	
	def __init__(self):
		self.reset()
		
	def get(self):
		return self.count
		
	def add(self, amount):
		self.count += amount
		
	def newlevel(self):
		self.ms = 0
		self.clock = pygame.time.Clock()
		self.clock.tick()
		
	def scorelevel(self):
		self.ms += self.clock.tick()
		self.add(max(0, int((self.__time_baseline - self.ms) / self.__ms_per_point)))
		self.newlevel()
		
	def startpause(self):
		self.ms += self.clock.tick()
		
	def endpause(self):
		self.clock.tick()
		
	def reset(self):
		self.count = 0
		self.newlevel()

score = Score()
		