from __future__ import division

import pygame
import sys
import math
import random

import vector

from visible import *
from score import *


class School(object):
	# Maximum distance from the group center the Guppies can spawn
	__radius_max = 48
	
	__velocity_max = 64
	
	__view_buffer = 156
	
	__guppy_min = 8
	__guppy_max = 12
	
	list = []
	
	def __init__(self, pos):
		self.list.append(self)
		
		self.destroy = False
		
		self.members = []
		
		count = random.randint(self.__guppy_min, self.__guppy_max)
		
		self.rect = pygame.Rect(pos, (1, 1))
		
		for i in range(count):
			angle = math.radians(i * 360/count)
			dist = self.__radius_max
			self.members.append(Guppy((pos[0] + dist * math.cos(angle), pos[1] + dist * math.sin(angle))))
			
	def update(self, delta, view):
		#centerx, centery = 0, 0
		#velocityx, velocityy = 0, 0
	
		b = view.copy()
		b.width -= 2 * self.__view_buffer
		b.centerx += self.__view_buffer
		b.height += 2 * self.__view_buffer
		b.centery -= self.__view_buffer
	
		for g in self.members:
			if g.rect.colliderect(view):
				# Determine which others are visible
				l = [x for x in self.members if x != g and g.can_see(x) and not x.whirl]
			
				if len(l):
					g.bound(b)
					g.flock(l, delta)
			
	def draw(self, target, view):
		pass
	

class Guppy(Visible):

	#initalize Guppy using Visible parameters
	sprite_path = "gfx/guppy.png"
	sprite_res = (26, 40)
	sprite_solid = Subsprite(0, 2)
	
	__hp_max = 1
	list = []
	
	__velocity_max = 80.0
	__force_max = 1.25
	
	__cohesion_factor = 1.125
	__separation_factor = 10.0
	__rate_factor = 0.75
	
	__bound_factor = 10.0
	__avoid_factor = 2.0
	
	__separation_limit = 52
	
	__vis_radius = 128
	__vis_angle = math.radians(250)
	
	score = 10
	
	def __init__(self, loc):
		"""Create a guppy"""
		
		super(Guppy, self).__init__()

		self.set_animation(self.sprite_solid, 7)
		self.set_position(loc)
		self.list.append(self)
		self.__hp = self.__hp_max
		
		self.velocity = (random.uniform(-20.0, 20.0), random.uniform(80.0, 120.0))
		
		self.direction = math.radians(270)
		
		self.target = None
		self.whirl = False
		
	def update(self, delta, view):
		"""Updates Location"""
		super(Guppy, self).update(delta)
		
		# Move based on School
		if self.whirl:
			v = (self.target.centerx - self.rect.centerx, self.target.centery - self.rect.centery)
			mag = vector.mag(v)
			if mag < 300 * delta:
				self.rect.center = self.target.center
			else:
				v = vector.muls(vector.divs(v, vector.mag(v)), 300 * delta)
				self.move(v)
		else:
			self.rect.center = vector.add(self.rect.center, vector.muls(self.velocity, delta))
		
		#move down at constant rate
		#self.move((0, self.__speed[1] * delta))
		
	def damage(self, dam):
		"""Decrements health by a set number"""
		self.__hp -= dam
		if self.__hp <= 0:
			if not self.destroy:
				self.destroy = True
				score.add(self.score)
	
	def can_see(self, other):
		if vector.mag2(vector.sub(other.rect.center, self.rect.center)) <= self.__vis_radius ** 2:
			angle = vector.dir(vector.sub(other.rect.center, self.rect.center)) - (self.direction - self.__vis_angle / 2) % math.radians(360)
			if angle < self.__vis_angle:
				return True
		return False
	
	def steer(self, v):
		diff = vector.sub(v, self.rect.center)
		dist = vector.mag(diff)
		
		if dist > 0:
			diff = vector.divs(diff, dist)
			
			damp = 64.0
			if dist < damp:
				diff = vector.muls(diff, self.__velocity_max * (dist / damp))
			else:
				diff = vector.muls(diff, self.__velocity_max)
			
			vec = vector.sub(diff, self.velocity)
			vecdist = vector.mag(vec)
			if vecdist > self.__force_max:
				vec = vector.muls(vector.divs(vec, vecdist), self.__force_max)
		else:
			vec = (0, 0)
		
		return vec
		
	def flock(self, l, delta):
	
		v1 = vector.muls(self.cohesion(l), self.__cohesion_factor)
		v2 = vector.muls(self.separation(l), self.__separation_factor)
		v3 = vector.muls(self.rate(l), self.__rate_factor)

		self.velocity = vector.add(self.velocity, v1, v2, v3)
		
		self.velocity = vector.maxs(vector.mins(self.velocity, self.__velocity_max), -self.__velocity_max)
		
		self.direction = vector.dir(vector.add(self.velocity, (0, 192 / 6)))
		self.set_rotation(-math.degrees((self.direction - math.radians(90)) % math.radians(360)))
		
	
	# Boid functions
	def cohesion(self, l):
		v = (0, 0)
		for i in l:
			v = vector.add(v, i.rect.center)
		v = vector.divs(v, len(l))
		
		return self.steer(v)
		
		
	def separation(self, list):
		mean = (0.0, 0.0)
		for i in list:
			dist = vector.mag(vector.sub(self.rect.center, i.rect.center))
			if dist > 0 and dist < self.__separation_limit:
				mean = vector.add(mean, vector.divs(vector.sub(self.rect.center, i.rect.center), dist))
				
		return vector.divs(mean, len(list))
		
	def rate(self, list):
		mean = (0, 0)
		for i in list:
			mean = vector.add(mean, i.velocity)
		
		mean = vector.divs(mean, len(list))
		
		meandist = vector.mag(mean)
		if meandist > self.__force_max:
			mean = vector.muls(vector.divs(mean, meandist), self.__force_max)
		
		return mean
		
	def avoid(self, objs):
		v = (0, 0)
		for o in objs:
			pass
		
	def bound(self, area):
		v = (0, 0)
		diff = area.left - self.rect.left
		if diff > 0:
			v = vector.add(v, (diff, 0))
		diff = self.rect.right - area.right
		if diff > 0:
			v = vector.sub(v, (diff, 0))
		diff = area.top - self.rect.top
		if diff > 0:
			v = vector.add(v, (0, diff))
		diff = self.rect.bottom - area.bottom
		if diff > 0:
			v = vector.sub(v, (0, diff))
		
		self.velocity = vector.add(self.velocity, vector.muls(v, self.__bound_factor))
		
		#return v