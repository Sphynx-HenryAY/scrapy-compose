
from abc import ABC as AbstractClass, abstractproperty, abstractmethod

from ..base.fields import Field

class ParserField( Field ):

	from scrapy.utils.project import get_project_settings
	
	accept_syntax = [ "css", "xpath" ]
	suff_len = 5

	syntax = get_project_settings().get( "DEFAULT_SYNTAX", "css" )
	process_timing = []

	_context = None

	def __init__( self, syntax = None, **kwargs ):
		super().__init__( **kwargs )

		if syntax is not None:
			if syntax in self.accept_syntax:
				self.syntax = syntax
			else:
				raise TypeError( f"{syntax} is not accepted." )

		if self.process_timing:
			self._init_processors()

		self.composed = self.get_context

	def _init_processors( self ):

		from scrapy_compose.processors.compose import ProcessorCompose

		v = self.value

		for timing in self.process_timing:
			setattr( self, timing, ProcessorCompose( configs = v.get( timing ) ) )

	def get_context( self, response ):
		pass

	def get_selector( self, response ):
		return getattr( response, self.syntax )

class FuncField( ParserField ):

	func = None

	def __init__( self, **kwargs ):
		super().__init__( **kwargs )

		# self would not be passed to func call
		self.func = self.__class__.func

	def get_context( self, response ):
		return self.make_field(
			self.get_selector( response ),
			key = self.key,
			**self.value
		)

	@abstractmethod
	def make_field( self, selector, _type = None, key = None, **kwargs):
		pass
