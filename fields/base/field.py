
from abc import ABC as AbstractClass, abstractmethod
from copy import deepcopy

class Field( AbstractClass ):

	key = None
	value = None

	_context = None

	def __init__( self, key = None, value = None, **kwargs ):
		self.key = key
		value = deepcopy( value )

		if isinstance( value, dict ):
			self.meta = value.pop( "_meta", {} )
		else:
			self.meta = {}

		self.value = value
