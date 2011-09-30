from __future__ import division

import pygame
import sys
import random

from score import *
from salmon import *
from bubble import *
from rock import *
from log import *
from map import *
from fish import *
from bear import *
from eagle import *
from guppy import *
from catfish import *
from whirlpool import *
from whitbox import *
from waterfall import *
from boss import *


class Game(object):
	wres = 768
	#hres = 960
	hres = 864
	
	fps = 60
	
	__level_transition = None
	__level_transition_path = "gfx/levelcomplete.png"
	
	__fish_per_second = 1.0
	__school_per_second = 0.125
	__catfish_per_second = 0.25
	
	__stamina_bar_len = 120
	__health_bar_len = 120
	__sprite_health = None
	__sprite_health_path = "gfx/health.png"
	__health_dot_rad = 15
	
	__boss_bar_len = 240
	
	__final_heal = False
	
	# Orig. 192
	__scroll_min = 160
	__scroll_max = 240
	
	__map_names = ["level/01.png", "level/02.png", "level/03.png"]
	__num_maps = 3
	__sprite_pause = None
	__sprite_pause_path = "gfx/pause.png"
	
	__sprite_menu = None
	__sprite_menu_path = "gfx/menu.png"
	
	__sprite_river0 = None
	__sprite_river0_path = "gfx/river0.png"
	
	__sprite_river1 = None
	__sprite_river1_path = "gfx/river1.png"
	
	__sprite_dead = None
	__sprite_dead_path = "gfx/dead.png"
	
	__sprite_win = None
	__sprite_win_path = "gfx/win.png"
	
	__sprite_health = None
	__sprite_health_path = "gfx/health.png"
	
	sound_hit = None
	sound_hit_path = "snd/hit.wav"
	
	sound_win = None
	sound_win_path = "snd/finale.wav"
	
	#__guppy_spawn_rate = 1
	#__guppy_chance = 200
	
	def __init__(self):
		random.seed()
	
		pygame.init()
		pygame.mixer.init()
		
		self.screen = pygame.display.set_mode((self.wres, self.hres), pygame.FULLSCREEN)
		self.clock = pygame.time.Clock()
		
		#self.map = [Map("level/02.png"), Map("level/03.png"), Map("level/01.png")]
		
		self.__map_index = 1
		self.__map_number = 0
		#self.map2 = [Map("level/02.png")]
		#self.map3 = [Map("level/03.png")]
		
		
		# Objects
		#self.score = Score()
		
		
		#self.salmon = Salmon((0, 0))
		
		self.transition_amnt = 0.0
		self.transition = False
		self.restart = False
		
		
		
		
		if not self.__level_transition:
			self.__level_transition = pygame.image.load(self.__level_transition_path).convert_alpha()
		if not self.__sprite_pause:
			self.__sprite_pause = pygame.image.load(self.__sprite_pause_path).convert_alpha()
		if not self.__sprite_menu:
			self.__sprite_menu = pygame.image.load(self.__sprite_menu_path).convert_alpha()
		if not self.__sprite_river0:
			self.__sprite_river0 = pygame.image.load(self.__sprite_river0_path).convert_alpha()
		if not self.__sprite_river1:
			self.__sprite_river1 = pygame.image.load(self.__sprite_river1_path).convert_alpha()
		if not self.__sprite_dead:
			self.__sprite_dead = pygame.image.load(self.__sprite_dead_path).convert_alpha()
		if not self.__sprite_win:
			self.__sprite_win = pygame.image.load(self.__sprite_win_path).convert_alpha()
		if not self.__sprite_health:
			self.__sprite_health = pygame.image.load(self.__sprite_health_path).convert_alpha()
			
		if not self.sound_hit:
			self.sound_hit = pygame.mixer.Sound(self.sound_hit_path)
		if not self.sound_win:
			self.sound_win = pygame.mixer.Sound(self.sound_win_path)
		
		self.font = pygame.font.SysFont("Impact", 32)
			
		paused = True
		self.screen.blit(self.__sprite_menu, (0, 0), self.__sprite_pause.get_rect())
		pygame.display.flip()
		while paused:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						sys.exit()
					elif event.key == pygame.K_2:
						self.__map_number = 1
						self.__map_index = 2
						paused = False
					elif event.key == pygame.K_3:
						self.__map_number = 2
						self.__map_index = 3
						paused = False
					else:
						paused = False
		self.clock.tick(self.fps)
		
		score.newlevel()

		self.map1 = [Map(self.__map_names[self.__map_number], self.__num_maps - self.__map_index)]
		#self.map1 = [Map(self.__map_names[2], 0)]
		self.maps = [self.map1]
		
		#self.salmon = Salmon((self.maps[self.__map_index - self.__map_number - 1][0].width / 2, self.maps[self.__map_index - self.__map_number - 1][0].height -48))
		self.salmon = Salmon((self.maps[self.__map_index - self.__map_number - 1][0].width / 2, self.maps[self.__map_index - self.__map_number - 1][0].height -200))
		self.view = pygame.Rect((0, self.maps[self.__map_index - self.__map_number - 1][0].height - self.hres), (self.wres, self.hres))
		
		self.objects = [Waterfall.list, Splash.list, Whirlpool.list, WHitbox.list, Rock.list, Log.list, Fish.list, Bear.list, EagleSpawner.list, School.list, Guppy.list, Catfish.list, Boss.list, Bubble.list, WhirlAni.list, [self.salmon], Eagle.list]

	def update(self):
		# Handle collisions
		#if not self.salmon.getFlop() and not self.salmon.getBurst():
		
		for b in Bubble.list:
		
			for r in Rock.list:
			# Pop bubbles on rocks
				if b.rect.colliderect(r.rect):
					b.destroy = True
					break
					
			for l in Log.list:
				# Pop bubbles on logs
				if b.rect.colliderect(l.rect):
					b.destroy = True
					break
			
			for f in Fish.list:
				# Pop bubbles on fish and damage
				if b.rect.colliderect(f.rect):
					b.destroy = True
					
					f.damage(1)
					if f.destroy:
						self.sound_hit.play()
				
			for f in Catfish.list:
				if b.rect.colliderect(f.rect):
					b.destroy = True
					
					f.damage(1)
					if f.destroy:
						self.sound_hit.play()
			
			for g in Guppy.list:
				if b.rect.colliderect(g.rect):
					b.destroy = True
					
					g.damage(1)
					if g.destroy:
						self.sound_hit.play()
					
			for s in Boss.list:
				if b.rect.colliderect(s.rect):
					b.destroy = True
					s.damage(1)
		
		bounds = [pygame.Rect((self.view.left + 168, self.view.top), (self.view.width - 168 * 2, self.view.height / 2))]
		
		# Salmon collisions
		if self.salmon:
			if self.salmon.rect.top != 0 and not self.transition:
				if len(Waterfall.list) and self.salmon.rect.centery <= Waterfall.list[0].rect.bottom and not self.salmon.is_waterfall():
					self.salmon.rect.centery = Waterfall.list[0].rect.bottom
					self.salmon.do_waterfall()
		
			for r in Rock.list:
				if r.rect.colliderect(self.view):
					if not self.salmon.getFlop():
						if self.salmon.rect.colliderect(r.rect):
							self.salmon.damage(1)
					
				newbounds = []
				for b in bounds:
					if b.colliderect(r.rect):
						newbounds.append(pygame.Rect(b.topleft, (r.rect.left - b.left, b.height)))
						newbounds.append(pygame.Rect((r.rect.right, b.top), (b.right - r.rect.right, b.height)))
					else:
						newbounds.append(b)
				bounds[:] = newbounds
		
			
			for l in Log.list:
				if l.rect.colliderect(self.view):
					if not self.salmon.getFlop():
						if self.salmon.rect.colliderect(l.rect):
							self.salmon.damage(1)
				
				newbounds = []
				for b in bounds:
					if b.colliderect(l.rect):
						newbounds.append(pygame.Rect(b.topleft, (l.rect.left - b.left, b.height)))
						newbounds.append(pygame.Rect((l.rect.right, b.top), (b.right - l.rect.right, b.height)))
					else:
						newbounds.append(b)
				bounds[:] = newbounds
	
			# Only accept valid bounds
			bounds[:] = [b for b in bounds if b.width >= 24]
			
		
					
			for f in Fish.list:
				f.target = None
				if not f.whirl:
					f.target = self.salmon.rect
				if self.salmon.rect.colliderect(f.rect):
					if not self.salmon.getFlop() and not self.salmon.getBurst():
						self.salmon.damage(1)
						f.destroy = True
					
			for c in Catfish.list:
				if self.salmon.rect.colliderect(c.rect):
					if not self.salmon.getFlop() and not self.salmon.getBurst():
						self.salmon.damage(1)
						c.destroy = True
	
			for g in Guppy.list:
				if self.salmon and self.salmon.rect.colliderect(g.rect):
					if not self.salmon.getFlop() and not self.salmon.getBurst():
						self.salmon.damage(1)
						g.destroy = True
				for r in Rock.list:
					if g.rect.colliderect(r.rect):
						g.destroy = True
						break
				for l in Log.list:
					if g.rect.colliderect(l.rect):
						g.destroy = True
						break
		
			if self.salmon.getBurst():
				for f in Fish.list:
					if self.salmon:
						f.target = self.salmon.rect
			elif self.salmon.getFlop(): 
				for f in Fish.list:
					f.target = None
		
		for w in Whirlpool.list:
			#if w.active():
			for f in Fish.list:
					#if w.rect.colliderect(f.rect):
					if vector.mag2(vector.sub(w.rect.center, f.rect.center)) < 48 ** 2:
						f.destroy = True
						score.add(f.score)
				
			for c in Catfish.list:
					#if w.rect.colliderect(c.rect):
					if vector.mag2(vector.sub(w.rect.center, c.rect.center)) < 48 ** 2:
						c.destroy = True
						score.add(c.score)
				
			for g in Guppy.list:
					#if w.rect.colliderect(g.rect):
					if vector.mag2(vector.sub(w.rect.center, g.rect.center)) < 48 ** 2:
						g.destroy = True
						score.add(g.score)
			
		
		for wb in WHitbox.list:
			for f in Fish.list:
				if wb.rect.colliderect(f.rect):
					f.whirl = True
					f.target = wb.rect
			for g in Guppy.list:
				if wb.rect.colliderect(g.rect):
					g.whirl = True
					g.target = wb.rect
			for c in Catfish.list:
				if wb.rect.colliderect(c.rect):
					c.whirl = True
					c.target = wb.rect
			
			for b in Boss.list:
				if wb.rect.colliderect(b.rect):
					b.whirl = True
					b.target = wb.rect
					wb.destroy = True
		

		for e in Eagle.list:
			e.target = None
			if self.salmon:
				e.target = self.salmon.rect
				if self.salmon.rect.colliderect(e.rect):
					if e.is_attacking():
						#EagleSpawner.sound_caw.play()
						self.salmon.damage(5)
		for b in Bear.list:
			br = pygame.Rect((0, b.rect.top), (self.view.width, b.rect.height))
			if self.salmon:
				if self.salmon.rect.colliderect(br):
					b.attack()
				if self.salmon.rect.colliderect(b.rect):
					self.salmon.damage(5)
					
		for b in Boss.list:
			if self.salmon:
				if self.salmon.rect.colliderect(b.rect):
					self.salmon.damage(5)
		
		# Get the number of (hopefully) fractional seconds since last loop
		delta = float(self.clock.tick(self.fps)) / 1000
		
		self.handle_events()
				
		for l in self.objects:
			for o in l:
				o.update(delta, self.view)
		
		if self.view.top > 240 or len(Boss.list):
			fish = self.__fish_per_second * delta
			fish = int(math.floor(fish) + (random.random() < math.fmod(fish, 1.0)))
			school = self.__school_per_second * delta
			school = int(math.floor(school) + (random.random() < math.fmod(school, 1.0)))
			catfish = self.__catfish_per_second * delta
			catfish = int(math.floor(catfish) + (random.random() < math.fmod(catfish, 1.0)))
		
			if len(bounds):
				for i in range(fish):
					b = random.choice(bounds)
					Fish((random.randint(b.left + 0, b.right - 24), self.view.top - 48))
				
				for i in range(school):
					b = random.choice(bounds)
					School((random.randint(b.left + 0, b.right - 24), self.view.top - 48))
				
				for i in range(catfish):
					b = random.choice(bounds)
					c = Catfish((random.randint(b.left + 0, b.right - 24), self.view.top - 48))
					c.target = self.salmon.rect
					c.bound = b
		
		scroll = 0
		if self.salmon:
			scroll = self.__scroll_min + (self.__scroll_max - self.__scroll_min) * (1 - (self.salmon.rect.centery - self.view.top) / self.hres)
			if self.salmon.getBurst():
				scroll = scroll * 2
		
		self.view.top -= scroll * delta
		for b in Boss.list:
			if b.rect.colliderect(self.view):
				b.rect.top -= scroll * delta
				if not self.__final_heal:
					self.salmon.replenish()
					self.__final_heal = True
				if not b.whirl and b.target:
					b.target.top -= scroll * delta
		
		if not len(Boss.list):
			self.view.top = max(0, self.view.top)
		
		if self.salmon.rect.top == 0 and not len(Boss.list):
			self.transition = True
			#self.salmon.move((0, -1000))
			#while self.transition_amnt < self.__max_transition:
			#	self.view.top -= scroll * 2
			#	print self.salmon.rect.top
				#print self.transition_amnt
			#	self.transition_amnt += scroll * 2 * delta
				#self.clock.tick(self.fps)
				
				
			
			
			#if self.transition_amnt >= self.__max_transition:
			#print "true"
				#self.transition = True
				#self.transition_amnt = 0.0
				
		for b in Boss.list:
			if b.destroy:
				score.scorelevel()
				self.sound_win.play()
				
				paused = True
				self.screen.blit(self.__sprite_win, (0, 0), self.__sprite_win.get_rect())
				t = self.font.render(str(score.get()), True, (0, 0, 0, 255))
				self.screen.blit(t, (350, 500), t.get_rect())
				
				pygame.display.flip()
				while paused:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							sys.exit()
						elif event.type == pygame.KEYDOWN:
							if event.key == pygame.K_ESCAPE:
								sys.exit()
		
		for l in self.objects:
			l[:] = [x for x in l if x.rect.top <= self.view.bottom and x.destroy == False]
			
		if not self.salmon or self.salmon.destroy:
			paused = True
			self.screen.blit(self.__sprite_dead, (0, 0), self.__sprite_dead.get_rect())
			t = self.font.render(str(score.get()), True, (255, 255, 255, 255))
			self.screen.blit(t, (350, 500), t.get_rect())
			
			pygame.display.flip()
			while paused:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							sys.exit()
						elif event.key == pygame.K_SPACE:
							score.reset()
							for l in self.objects:
								if not len(l) or l[0] != self.salmon:
									l[:] = []
									#for i in range(len(l)):
									#	del l[i]
							return -1
		
							
		
	def draw(self):
	
		#if not self.__map_switch:
			#self.map[1].create()
			#self.__map_switch = True
		if self.transition:
			stall = True
			for w in Waterfall.list:
				w.sound_waterfall.stop()
			while stall:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							sys.exit()
						else:
							stall = False
				self.screen.blit(self.__level_transition, (0,0), self.__level_transition.get_rect())
				pygame.display.flip()
				self.clock.tick(self.fps)
			if self.__num_maps > self.__map_index:
				"""for i in Waterfall.list:
					i.destroy = True
				for i in Whirlpool.list:
					i.destroy = True
				for i in Fish.list:
					i.destroy = True
				for i in Catfish.list:
					i.destroy = True
				for i in Guppy.list:
					i.destroy = True
				for i in Eagle.list:
					i.destroy = True
				for i in Bear.list:
					i.destroy = True"""
				for l in self.objects:
					if not len(l) or l[0] != self.salmon:
						l[:] = []
						#for i in range(len(l)):
						#	del l[i]
				
				
				self.__map_index += 1
				new_map = [Map(self.__map_names[self.__map_index - 1], self.__num_maps - self.__map_index)]
				#new_map[0].create()
				self.maps.append(new_map)
				self.view.bottom = new_map[0].height + 2000
				self.salmon.set_position((self.maps[self.__map_index - self.__map_number - 1][0].width / 2, self.view.bottom - 300))
				self.salmon.action = {"left":False, "right":False, "up":False, "down":False, "bubble":False, "whirlpool":False, "flop":False, "burst":False}
				self.salmon.set_animation(self.salmon.sprite_swim, 10)
				self.salmon.replenish()
				self.transition = False
				self.restart = False

				
				
		# Background
		self.screen.fill(self.maps[self.__map_index - self.__map_number - 1][0].color_water)

		pygame.draw.rect(self.screen, self.maps[self.__map_index - self.__map_number - 1][0].color_grass, pygame.Rect((0, 0), (6 * self.maps[self.__map_index - self.__map_number - 1][0].blocksize, self.hres)))
		pygame.draw.rect(self.screen, self.maps[self.__map_index - self.__map_number - 1][0].color_grass, pygame.Rect((self.wres - (6 * self.maps[self.__map_index - self.__map_number - 1][0].blocksize), 0), (6 * self.maps[self.__map_index - self.__map_number - 1][0].blocksize, self.hres)))
		
		
		
		self.screen.blit(self.__sprite_river0, (0, -(self.view.bottom % self.hres)), self.__sprite_river0.get_rect())
		self.screen.blit(self.__sprite_river0, (0, self.hres - self.view.bottom % self.hres), self.__sprite_river0.get_rect())
		
		
		for l in self.objects:
			for i in l:
				i.draw(self.screen, self.view)
				
		
		
		#stamina and health bars
		if self.salmon:		
			health_specs = self.salmon.getDamage()
			if health_specs[0] != health_specs[1]:
				for i in range(0, health_specs[1] - health_specs[0]):
					#pygame.draw.circle(self.screen, (255, 0, 0), (65 + (self.__health_dot_rad * i * 2), 100), self.__health_dot_rad)
					self.screen.blit(self.__sprite_health, (4 + (i * self.__sprite_health.get_width()), 4), self.__sprite_health.get_rect())
			
			stam_specs = self.salmon.getStamina()
			c = pygame.Color(255, 255, 255, 255)
			
			c.hsva = (25, 50 + 50 * (stam_specs[0]/stam_specs[1]), 90, 100)
			pygame.draw.rect(self.screen, c, (4, 4 + 30 + 6, self.__stamina_bar_len * (stam_specs[0] / stam_specs[1]), 24))
			pygame.draw.line(self.screen, (0, 0, 0, 255), (4 + self.__stamina_bar_len, 4 + 30 + 6), (4 + self.__stamina_bar_len, 4 + 30 + 6 + 24))
		if Boss.list:	
			if Boss.list[0].rect.colliderect(self.view):
				health_specs = Boss.list[0].getDamage()
				l = self.__boss_bar_len * ((health_specs[1] - health_specs[0]) / health_specs[1])
				pygame.draw.rect(self.screen, (184, 138, 0), (self.wres - 4 - l, 4, l, 24))
				pygame.draw.line(self.screen, (0, 0, 0, 255), (self.wres - 4 - self.__boss_bar_len, 4), (self.wres - 4 - self.__boss_bar_len, 4 + 24))
		
				
		s = self.font.render(str(score.get()), True, pygame.Color(0, 0, 0, 255))
		self.screen.blit(s, (4, 4 + 30 + 6 + 24 + 6), s.get_rect())
		
		# Flip buffer
		pygame.display.flip()
		
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
				elif event.key == pygame.K_p:
					self.pause()
						
				if self.salmon:
					if event.key == pygame.K_RIGHT:
						self.salmon.action['right'] = True
					elif event.key == pygame.K_LEFT:
						self.salmon.action['left'] = True
					elif event.key == pygame.K_UP:
						self.salmon.action['up'] = True
					elif event.key == pygame.K_DOWN:
						self.salmon.action['down'] = True
					elif event.key == pygame.K_z:
						self.salmon.action['bubble'] = True
					elif event.key == pygame.K_x:
						self.salmon.action['whirlpool'] = True
					elif event.key == pygame.K_c:
						self.salmon.action['flop'] = True
					elif event.key == pygame.K_SPACE:
						self.salmon.action['burst'] = True
					
			elif event.type == pygame.KEYUP:
				if self.salmon:
					if event.key == pygame.K_RIGHT:
						self.salmon.action['right'] = False
					elif event.key == pygame.K_LEFT:
						self.salmon.action['left'] = False
					elif event.key == pygame.K_UP:
						self.salmon.action['up'] = False
					elif event.key == pygame.K_DOWN:
						self.salmon.action['down'] = False
					elif event.key == pygame.K_z:
						self.salmon.action['bubble'] = False
					elif event.key == pygame.K_x:
						self.salmon.action['whirlpool'] = False
					elif event.key == pygame.K_c:
						self.salmon.action['flop'] = False
					elif event.key == pygame.K_SPACE:
						self.salmon.action['burst'] = False

	def pause(self):
		score.startpause()
		paused = True
		self.screen.blit(self.__sprite_pause, (0, 0), self.__sprite_pause.get_rect())
		pygame.display.flip()
		while paused:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						sys.exit()
					elif event.key == pygame.K_p:
						paused = False
			
		self.salmon.action = {"left":False, "right":False, "up":False, "down":False, "bubble":False, "whirlpool":False, "flop":False, "burst":False}
		self.clock.tick(self.fps)
		score.endpause()