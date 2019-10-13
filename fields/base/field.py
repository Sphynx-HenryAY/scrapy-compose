
from abc import ABC as AbstractClass, abstractmethod
from copy import deepcopy

class Field( AbstractClass ):

	from scrapy_compose.utils import classproperty

	sufx_len = 0
	composed = None

	key = None
	value = None

	def __init__( self, key = None, value = None, **kwargs ):
		self.key = key
		value = deepcopy( value )

		if isinstance( value, dict ):
			self.meta = value.pop( "_meta", {} )
		else:
			self.meta = {}

		self.value = value

	@classproperty
	def fkey( cls ):
		return cls.__name__[:-cls.suff_len].lower()

	def __call__( self, *args, **kwargs ):
		return self.composed( *args, **kwargs )

