
from abc import ABC as AbstractClass, abstractproperty, abstractmethod

from ..base.field import Field

class ParserField( Field ):
	
	selector = None
	sanitize_timing = []

	def __init__( self, key = None, value = None, selector = None, **kwargs ):
		super().__init__( key = key, value = value )

		self.selector = selector

		if self.sanitize_timing:
			self._init_sanitizers()

	def _init_sanitizers( self ):

		from scrapy_compose.load import resource as load_resource

		v = self.value

		def default_sntz( x ): return x

		for timing in self.sanitize_timing:

			sntz_paths = v.get( timing )

			if sntz_paths:
				if isinstance( sntz_paths, str ):
					sntz = load_resource( sntz_paths )
				elif isinstance( sntz_paths, list ):
					def sntz( x ):
						for path in sntz_paths:
							x = load_resource( path )( x )
						return x
				else:
					raise TypeError( f"{type(sntz_paths).title()} of sanitizers is not supported." )
			else:
				sntz = default_sntz

			setattr( self, timing, sntz )

	@property
	def syntax( self ):
		return self.selector.__name__

	def reuse( self, selector ):
		self._context = None
		self.selector = selector
		return self

class FuncField( ParserField ):

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
