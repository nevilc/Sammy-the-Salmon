from __future__ import division

class Subsprite(object):
	"""Indicates a single animation of a sprite (i.e. a single row)"""
	def __init__(self, position, frames):
	
		# The vertical position of the animation on the sheet
		self.position = position
		# The horizontal length of the animation
		self.frames = frames
	
