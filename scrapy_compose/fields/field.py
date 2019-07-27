
from abc import ABC as AbstractClass, abstractproperty, abstractmethod

class Field( AbstractClass ):

	key = None
	value = None
	selector = None

	_content = None

	def __init__( self, key = None, value = None, selector = None ):
		self.key = key
		self.value = value
		self.selector = selector

	@abstractproperty
	def content( self ): pass

	@property
	def syntax( self ):
		return self.selector.__name__

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
