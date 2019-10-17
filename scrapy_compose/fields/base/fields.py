
from abc import ABC as AbstractClass, abstractmethod

class Field( AbstractClass ):

	from scrapy_compose.utils import classproperty

	sufx_len = 0
	composed = None

	key = None
	value = None

	def __init__( self, key = None, value = None, **kwargs ):
		from copy import deepcopy

		if key is not None:
			self.key = key

		if value is not None:
			self.value = value

		value = deepcopy( self.value )

		self.meta = value.pop( "_meta", {} )
		self.value = value

	@classproperty
	def fkey( cls ):
		return cls.__name__[:-cls.suff_len].lower()

	def __call__( self, *args, **kwargs ):
		return self.composed( *args, **kwargs )

class Fields:

	from scrapy_compose.utils import classproperty

	_fields = None
	Field = Field

	@classproperty
	def fields( cls ):
		if cls._fields is None:
			cls._fields = {}
		return cls._fields

	@classmethod
	def register( cls, field ):
		from inspect import isclass
		base_field = cls.Field
		if (
				isclass( field ) and
				issubclass( field, base_field ) and
				field is not base_field
			):
			setattr( cls, field.__name__, field )
			cls.fields[ field.fkey ] = field
			return field
