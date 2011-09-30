from __future__ import division

import math

def mag2(v):
	"""Vector magnitude squared (for cheaper distance comparisons)"""
	sum = 0.0
	for i in v:
		sum += i ** 2
	return sum

def mag(v):
	"""Vector magnitude"""
	return math.sqrt(mag2(v))
	
def dir(v):
	"""Vector direction in radians (2D vectors only)"""
	return math.atan2(v[1], v[0])

def _ops(op, v, s):
	"""Perform an operation on a vector and a series of scalars"""
	
	l = list(v)
	for i in s:
		for j in range(len(l)):
			l[j] = op(l[j], i)
		
	return tuple(l)
	
def _op(op, v):
	"""Perform an operation sequentially on members of vectors"""
	size = None
	for t in v:
		if size == None:
			size = len(t)
		elif size != len(t):
			# Error, tuples must be of same size
			return ()
		
	if len(v) == 0:
		# Error
		return ()
	
	result = None
	for i in v:
		if result == None:
			result = list(i)
		else:
			for a, j in enumerate(i):
				result[a] = op(result[a], j)
		
	return tuple(result)
	
def add(*v):
	return _op(lambda x, y: x + y, v)
	
def sub(*v):
	return _op(lambda x, y: x - y, v)
	
def mul(*v):
	return _op(lambda x, y: x * y, v)
	
def div(*v):
	return _op(lambda x, y: x / y, v)

def pow(*v):
	return _op(lambda x, y: x ** y, v)
	
def max(*v):
	return _op(lambda x, y: x >= y and x or y, v)

def min(*v):
	return _op(lambda x, y: x <= y and x or y, v)
	
def adds(v, *s):
	return _ops(lambda x, y: x + y, v, s)
	
def subs(v, *s):
	return _ops(lambda x, y: x - y, v, s)
	
def muls(v, *s):
	return _ops(lambda x, y: x * y, v, s)
	
def divs(v, *s):
	return _ops(lambda x, y: x / y, v, s)
	
def pows(v, *s):
	return _ops(lambda x, y: x ** y, v, s)
	
def maxs(v, *s):
	return _ops(lambda x, y: x >= y and x or y, v, s)

def mins(v, *s):
	return _ops(lambda x, y: x <= y and x or y, v, s)