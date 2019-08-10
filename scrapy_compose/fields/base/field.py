
from abc import ABC as AbstractClass, abstractproperty, abstractmethod

class Field( AbstractClass ):

	key = None
	value = None
	selector = None

	_context = None

	sanitize_timing = ()

	def __init__( self, key = None, value = None, selector = None, **kwargs ):
		self.key = key
		self.value = value
		self.selector = selector

		self._sntzs = {}

	@abstractproperty
	def context( self ): pass

	@property
	def sanitizers( self ):
		if not self._sntzs:
			self._init_sanitizers()
		return self._sntzs

	def _init_sanitizers( self ):

		from scrapy_compose.load import resource as load_resource

		v = self.value
		sntzs = self._sntzs

		default_sntz = lambda x: x

		for timing in self.sanitize_timing:

			sntz_paths = v.get( timing )

			if not sntz_paths:
				sntz = default_sntz
			else:
				if isinstance( sntz_paths, str ):
					sntz = load_resource( sntz_paths )
				elif isinstance( sntz_paths, list ):
					prv_sntz = None
					for path in sntz_paths:
						sntz = load_resource( path )

						if prv_sntz:
							_sntz = sntz
							sntz = lambda v: _sntz( prv_sntz( v ) )

						prv_sntz = sntz

			sntzs[timing] = sntz
			setattr( self, timing, sntz )

	@property
	def syntax( self ):
		return self.selector.__name__


class FuncField( Field ):

	func = None

	def __init__( self, key = None, value = None, selector = None, **kwargs ):
		super().__init__( key = key, value = value, selector = selector, **kwargs )

		# self would not be passed to func call
		self.func = self.__class__.func

	def __call__( self, *args, **kwargs ):
		return self.func( *args, **kwargs )

	@abstractmethod
	def make_field( self, selector, _type = None, key = None, **kwargs):
		pass

	@property
	def context( self ):
		if self._context is None:
			self._context = self._init_context()
		return self._context

	def _init_context( self ):
		return self.make_field(
			self.selector,
			key = self.key,
			**self.value
		)
