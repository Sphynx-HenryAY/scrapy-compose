
try:
	from abc import ABC as AbstractClass, abstractproperty, abstractmethod
except ImportError:
	from abc import ABCMeta, abstractproperty, abstractmethod
	AbstractClass = ABCMeta( "AbstractClass", (), {} )

from ..base.fields import Field

class ParserField( Field ):

	accept_syntax = [ "css", "xpath" ]
	suff_len = 5

	process_timing = []

	_context = None

	def __init__( self, syntax = None, **kwargs ):
		super( ParserField, self ).__init__( **kwargs )

		if syntax is not None:
			self.syntax = syntax
		elif "syntax" in self.meta:
			self.syntax = self.meta[ "syntax" ]
		else:
			from scrapy_compose.compose_settings import DEFAULT_SYNTAX
			self.syntax = DEFAULT_SYNTAX

		if self.syntax not in self.accept_syntax:
			raise TypeError( syntax + " is not accepted." )

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

	def __init__( self, **kwargs ):
		super( FuncField, self ).__init__( **kwargs )

	def get_context( self, response ):
		return self.make_field(
			self.get_selector( response ),
			key = self.key,
			**self.value
		)

	@abstractmethod
	def make_field( self, selector, _type = None, key = None, **kwargs):
		pass
