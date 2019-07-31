
from functools import lru_cache
from abc import ABC as AbstractClass, abstractproperty, abstractmethod

class Field( AbstractClass ):

	key = None
	value = None
	selector = None

	_content = None

	sanitize_timing = ()

	def __init__( self, key = None, value = None, selector = None ):
		self.key = key
		self.value = value
		self.selector = selector

		self._sntzs = {}

	@abstractproperty
	def content( self ): pass

	@property
	def sanitizers( self ):
		if not self._sntzs:
			self._init_sanitizers()
		return self._sntzs

	def _init_sanitizers( self ):

		v = self.value
		sntzs = self._sntzs
		load_rsrc = self.load_resource

		default_sntz = lambda x: x

		for timing in self.sanitize_timing:

			sntz_paths = v.get( timing )

			if not sntz_paths:
				sntz = default_sntz
			else:
				if isinstance( sntz_paths, str ):
					sntz = load_rsrc( sntz_paths )
				elif isinstance( sntz_paths, list ):
					prv_sntz = None
					for path in sntz_paths:
						sntz = load_rsrc( path )

						if prv_sntz:
							_sntz = sntz
							sntz = lambda v: _sntz( prv_sntz( v ) )

						prv_sntz = sntz

			sntzs[timing] = sntz
			setattr( self, timing, sntz )

	@property
	def syntax( self ):
		return self.selector.__name__

	@lru_cache( maxsize = 64 )
	def load_resource( self, path ):
		from importlib import import_module
		mod, func = path.rsplit( ".", 1 )
		return getattr( import_module( mod ), func )


class FuncField( Field ):

	func = None

	def __init__( self, key = None, value = None, selector = None ):
		super().__init__( key = key, value = value, selector = selector )

		# self would not be passed to func call
		self.func = self.__class__.func

	def __call__( self, *args, **kwargs ):
		return self.func( *args, **kwargs )

	@abstractmethod
	def make_field( self, selector, _type = None, key = None, **kwargs):
		pass

	@property
	def content( self ):
		if self._content is None:
			self._content = self._init_content()
		return self._content

	def _init_content( self ):
		return self.make_field(
			self.selector,
			key = self.key,
			**self.value
		)
