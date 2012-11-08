from __future__ import division

import pygame
import math

from visible import *
from bubble import *
from whirlpool import *
from score import *

class Splash(Visible):
	sprite_path = "gfx/splash.png"
	sprite_res = (179, 140)
	sprite_animate = Subsprite(0, 7)
	
	sound_splash_path = "snd/splash.wav"
	sound_splash = None
	
	list = []
	
	def __init__(self, pos):
		super(Splash, self).__init__()
		
		self.set_position(pos)
		
		self.set_animation(self.sprite_animate, 10)
		
		self.list.append(self)
		
		if not self.sound_splash:
			self.sound_splash = pygame.mixer.Sound(self.sound_splash_path)
		self.sound_splash.play()
		
	def update(self, delta, view):
		super(Splash, self).update(delta)
		if self.frame >= 10:
			self.destroy = True
		
class WhirlAni(Visible):
	sprite_path = "gfx/salmon_spin.png"
	sprite_res = (78, 81)
	sprite_spin = Subsprite(0, 9)
	
	list = []
	
	def __init__(self, pos):
		super(WhirlAni, self).__init__()
		
		self.set_position(pos)
		
		self.set_animation(self.sprite_spin, 10)
		
		self.list.append(self)
	
	def update(self, delta, view):
		super(WhirlAni, self).update(delta)
		if self.frame >= 10:
			self.destroy = True

class Salmon(Visible):
	sprite_path = "gfx/salmon.png"
	sprite_res = (40, 83)
	sprite_swim = Subsprite(0, 8)
	
	sprite_idle = Subsprite(0, 8)
	
	sound_bubble_path = "snd/bubble_shoot.wav"
	sound_bubble = None
	
	sound_dead_path = "snd/dead.wav"
	sound_dead = None
	
	sound_hurt_path = "snd/hurt.wav"
	sound_hurt = None
	
	sound_dash_path = "snd/dash.wav"
	sound_dash = None
	
	# Move speed in pixels per second (horizontal, vertical)
	__speed = (280, 280)
	__drift = -20
	
	__acceleration = (640, 640)
	__velocity_decay = (960, 960)
	
	# Maximum rotation allowed in degrees
	__rotation_max = 15.0
	# Rotation speed in degrees per second
	__rotation_speed = 10.0
	# Rotation "decay," how quickly the fish returns to pointing forward (lower is faster)
	__rotation_decay = 0.85
	# Rotation threshold, if the rotation is less than this value, set it to zero
	# Prevents rotating the sprite very tiny amounts
	__rotation_threshold = 0.125
	
	# Maximum stamina
	__stamina_max = 60
	__stamina_regen = 3.0
	
	__whirlpool_cost = 20
	__flop_cost = 15
	__burst_cost = 20
	
	
	# Ability constants
	__bubble_interval = 0.20
	
	__whirlpool_interval = 5.0
	__whirlpool_speed = 500
	__whirlpool_distance = 500
	
	__flop_interval = 1.1
	__flop_radius = 100
	__flop_limit = 1.0
	
	__flop_scale_max = 1.25
	__flop_scale_speed = 0.25
	
	# Maximum hits before dying
	__dmg_max = 20
	
	# How many seconds of invulnerability after hitting an obstacle
	__invuln_limit = 1.5
	# Number of seconds a single 'blink' lasts when invulnerable
	__invuln_blink = 0.125
	
	
	__burst_limit = 4.0
	__burst_interval = 5.0
	
	
	
	def __init__(self, pos):
		super(Salmon, self).__init__()
		
		self.set_position(pos)
		#self.set_animation(self.sprite_idle, 4)
		self.set_animation(self.sprite_swim, 10)
		self.action = {"left":False, "right":False, "up":False, "down":False, "bubble":False, "whirlpool":False, "flop":False, "burst":False}
		
		self.__velocity = (0.0, 0.0)
		
		if not self.sound_bubble:
			self.sound_bubble = pygame.mixer.Sound(self.sound_bubble_path)
			
		if not self.sound_dead:
			self.sound_dead = pygame.mixer.Sound(self.sound_dead_path)
			
		if not self.sound_hurt:
			self.sound_hurt = pygame.mixer.Sound(self.sound_hurt_path)
			
		if not self.sound_dash:
			self.sound_dash = pygame.mixer.Sound(self.sound_dash_path)
		
		# Coordinates from last frame, used to determine velocity
		self.__prev = self.rect.topleft
		
		self.__dmg = 0
		self.__dmg_cap = int(self.__dmg_max / 2)
		
		self.__invuln_time = 0
		self.__burst_time = 0
		self.__flop_time = 0
		self.__stamina = self.__stamina_max
		self.__isFlop = False
		self.__isBurst = False
		self.__isWhirlpool = False
		
		self.__whirlpool_velocity = None
		
		# Ability cooldowns
		self.__bubble_cooldown = 0.0
		self.__whirlpool_cooldown = 0.0
		self.__flop_cooldown = 0.0
		self.__burst_cooldown = 0.0
		
		#self.ani_change = 0.0
		
		self.__waterfall = False
		
		self.__up_was_pushed = False
		
		#print(self.rect)
		#print("If we don't have a print here, the fish sometimes disappears!")
	
		
	def update(self, delta, view):
		super(Salmon, self).update(delta)
		
		# Get the x and y coordinates from before moving to calculate current velocity
		self.__prev = self.rect.center
		
		if self.__stamina < self.__stamina_max:
			self.__stamina += delta * self.__stamina_regen
		elif self.__stamina > self.__stamina_max:
			self.__stamina = self.__stamina_max
	
			
		
		self.__invuln_time -= delta
		self.__burst_time -= delta
		self.__flop_time -= delta
		
		if WhirlAni.list:
			WhirlAni.list[0].rect.center = self.rect.center
			Whirlpool.list[0].rect.center = self.rect.center
			WhirlAni.list[0].visible = self.__invuln_time <= 0 or math.floor(self.__invuln_time / self.__invuln_blink) % 2 
		if not WhirlAni.list and self.__isWhirlpool:
			self.__isWhirlpool = False
			Whirlpool.list[0].set_velocity(self.__whirlpool_velocity)
			Whirlpool.list[0].set_windup(False)
			
		if self.__isWhirlpool:
			self.visible = False
		else:
			self.visible = self.__invuln_time <= 0 or math.floor(self.__invuln_time / self.__invuln_blink) % 2 
		
		
			
		if self.__burst_time <= 0 and self.__isBurst:
			self.__isBurst = False
			self.set_animation(self.sprite_swim, 10)
		elif self.__burst_time > 0:
			self.action['bubble'] = False
			self.action['flop'] = False
			self.action['whirlpool'] = False
			
		if self.__flop_time <= 0 and self.__isFlop:
			self.__isFlop = False
			degrees = [0 , math.pi/4.0, math.pi/2.0, (3 * math.pi) / 4.0, math.pi, (5 * math.pi) / 4.0, (3 * math.pi) / 2.0, (7 * math.pi) / 4.0]
			for d in degrees:
				#Bubble((self.rect.topleft[0] + self.__flop_radius * math.cos(d), self.rect.topleft[1] + self.__flop_radius * math.sin(d)), (0,0), 0, 270 - self.get_rotation())
				boost = min(-2, (self.rect.centery - self.__prev[1])/delta)
				for i in range(1):
					Bubble((self.rect.topleft[0] + self.__flop_radius * math.cos(d), self.rect.topleft[1] + self.__flop_radius * math.sin(d)), (0, boost), d)
				s = Splash(self.rect.center)
				s.rect.center = self.rect.center
				
			self.__invuln_time = 0.01	
			self.set_animation(self.sprite_swim, 10)
			self.set_scale((1, 1))
		elif self.__flop_time > 0:
			self.action['left'] = False
			self.action['right'] = False
			self.action['burst'] = False
			self.action['bubble'] = False
			self.action['whirlpool'] = False
			
				
		#elif not self.visible:
		#		self.visible = True
		if self.__isFlop:
			s = min(self.__flop_scale_max, self.get_scale()[0] + self.__flop_scale_speed * delta)
			self.set_scale((s, s))
		self.__bubble_cooldown = max(0.0, self.__bubble_cooldown - delta)
		self.__whirlpool_cooldown = max(0.0, self.__whirlpool_cooldown - delta)
		self.__flop_cooldown = max(0.0, self.__flop_cooldown - delta)
		self.__burst_cooldown = max(0.0, self.__burst_cooldown - delta)
		
		if not self.__waterfall:
			#self.rect.top -= 160 * delta
			self.move((0, self.__drift * delta))
			
			if self.action['up']:
				self.up(delta)
			if self.action['down']:
				self.down(delta)
			if self.action['left']:
				self.left(delta)
			if self.action['right']:
				self.right(delta)
			if self.action['bubble']:
				self.bubble(delta)
			if self.action['whirlpool']:
				self.whirlpool(delta)
			if self.action['flop']:
				self.flop(delta)
			if self.action['burst']:
				self.burst(delta)
				
			if not self.action['left'] and not self.action['right']:
				if abs(self.__velocity[0]) < self.__velocity_decay[0] * delta:
					self.__velocity = (0, self.__velocity[1])
				elif self.__velocity[0] > 0:
					self.__velocity = (self.__velocity[0] - self.__velocity_decay[0] * delta, self.__velocity[1])
				else:
					self.__velocity = (self.__velocity[0] + self.__velocity_decay[0] * delta, self.__velocity[1])
			if not self.action['up'] and not self.action['down']:
				if abs(self.__velocity[1]) < self.__velocity_decay[1] * delta:
					self.__velocity = (self.__velocity[0], 0)
				elif self.__velocity[1] > 0:
					self.__velocity = (self.__velocity[0], self.__velocity[1] - self.__velocity_decay[1] * delta)
				else:
					self.__velocity = (self.__velocity[0], self.__velocity[1] + self.__velocity_decay[1] * delta)
			
				
			self.move((self.__velocity[0] * delta, self.__velocity[1] * delta))
		else:
			if self.action['up']:
				#self.__up_was_pushed = True
				self.action['up'] = False
				self.rect.top = max(self.rect.top - 5, 0)
				if self.rect.top == 0:
					#print("Winner!")
					score.scorelevel()
					self.__waterfall = False
					self.move((0, -self.rect.height * 2))
					score.newlevel()
				
		
		# Cap rotation and normalize
		self.set_rotation(min(max(self.get_rotation(), -self.__rotation_max), self.__rotation_max))
		if not self.action['left'] and not self.action['right']:
			self.set_rotation(self.get_rotation() * self.__rotation_decay)
			if abs(self.get_rotation()) < self.__rotation_threshold:
				self.set_rotation(0.0)
				
		# Bound to view
		#self.rect.left = max(self.rect.left, view.left)
		#self.rect.right = min(self.rect.right, view.right)
		self.rect.top = max(self.rect.top, view.top)
		self.rect.bottom = min(self.rect.bottom, view.bottom)
		
		self.rect.left = max(self.rect.left, 144)
		self.rect.right = min(self.rect.right, view.right - 144)
		
	
	def left(self, delta):
		self.__velocity = (self.__velocity[0] - self.__acceleration[0] * delta, self.__velocity[1])
		self.__velocity = (max(self.__velocity[0], -self.__speed[0]), self.__velocity[1])
		
		self.rotate(self.__rotation_speed * delta)
		
	def right(self, delta):
		self.__velocity = (self.__velocity[0] + self.__acceleration[0] * delta, self.__velocity[1])
		self.__velocity = (min(self.__velocity[0], self.__speed[0]), self.__velocity[1])
		
		self.rotate(-self.__rotation_speed * delta)
		
	def up(self, delta):
		self.__velocity = (self.__velocity[0], self.__velocity[1] - self.__acceleration[1] * delta)
		self.__velocity = (self.__velocity[0], max(self.__velocity[1], -self.__speed[1] / 1.6))
		
	def down(self, delta):
		self.__velocity = (self.__velocity[0], self.__velocity[1] + self.__acceleration[1] * delta)
		self.__velocity = (self.__velocity[0], min(self.__velocity[1], self.__speed[1]))
		
	def bubble(self, delta):
		# Wait until cooldown reaches 0, then create bubble
		if (self.__bubble_cooldown == 0.0) and (not self.__isFlop or not self.__isBurst):
			#Bubble(self.rect.topleft, ((self.rect.topleft[0] - self.__prev[0]) / delta, (self.rect.topleft[1] - self.__prev[1]) / delta), self.__bubble_speed, 270 - self.get_rotation())

			#Bubble(self.rect.center, vector.divs(vector.sub(self.rect.center, self.__prev) , delta), math.radians(270 - self.get_rotation()))
			self.sound_bubble.play()
			# Only shoot forward faster when moving
			boost = min(-3, (self.rect.centery - self.__prev[1])/delta)
			
			Bubble(self.rect.center, (0, boost), math.radians(270 - self.get_rotation()))
			self.__bubble_cooldown = self.__bubble_interval
	
	def whirlpool(self, delta):
		if(self.__whirlpool_cooldown == 0.0):
			if self.__stamina > self.__whirlpool_cost:
				self.__stamina -= self.__whirlpool_cost
				boost = min(-3, (self.rect.centery - self.__prev[1])/delta)
				#Whirlpool(self.rect.center, ((self.rect.topleft[0] - self.__prev[0]) / delta, (self.rect.topleft[1] - self.__prev[1]) / delta), math.radians(270 - self.get_rotation()))
				self.__whirlpool_velocity = (0, boost)
				Whirlpool(self.rect.center, (0, boost), math.radians(270 - self.get_rotation()))
				self.__whirlpool_cooldown = self.__whirlpool_interval
				WhirlAni(self.rect.center)
				self.__isWhirlpool = True
			else:
				print("Not enough stamina")
			
	
	def flop(self, delta):
		if(self.__flop_cooldown == 0.0):
			if self.__stamina > self.__flop_cost:
				self.__stamina -= self.__flop_cost
				self.__flop_time = self.__flop_limit
				self.__isFlop = True
				self.__flop_cooldown = self.__flop_interval
			else:
				print("Not enough stamina")
			
		#set_animation(self.sprite_flop, .5)
		
	def burst(self, delta):
		if (self.__burst_cooldown == 0.0):
			if self.__stamina > self.__burst_cost:
				self.__stamina -= self.__burst_cost
				self.__burst_time = self.__burst_limit
				self.__isBurst = True
				self.__burst_cooldown = self.__burst_interval
				self.action['left'] = False
				self.action['right'] = False
				self.set_animation(self.sprite_swim, 20)
				self.sound_dash.play()
			else:
				print("Not enough stamina")
			
	
	def damage(self, amount):
		if self.__invuln_time <= 0:
			self.__dmg += amount
			self.__invuln_time = self.__invuln_limit
			if self.__dmg >= self.__dmg_cap:
				self.destroy = True
				self.sound_dead.play()
			else:
				self.sound_hurt.play()
				
	def getFlop(self):
		return self.__isFlop
		
	def getBurst(self):
		return self.__isBurst
		
	def getStamina(self):
		self.__stamina = min(self.__stamina, self.__stamina_max)
		return (self.__stamina, self.__stamina_max)
		
	def getDamage(self):
		return (self.__dmg, self.__dmg_cap)
		
	def do_waterfall(self):
		self.__waterfall = True
		self.visible = True
		
		self.__invuln_time = 0
		self.__isFlop = False
		self.__isBurst = False
		self.set_animation(self.sprite_swim, 20)
		
		self.action = {"left":False, "right":False, "up":False, "down":False, "bubble":False, "whirlpool":False, "flop":False, "burst":False}
	
	def is_waterfall(self):
		return self.__waterfall
	
	def replenish(self):
		self.__dmg = 0
		
	def boss_replenish(self):
		self.__dmg_cap = self.__dmg_max
		self.__dmg = 0
		