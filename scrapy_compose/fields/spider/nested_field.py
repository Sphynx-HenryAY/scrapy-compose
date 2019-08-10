
from .fields import SpiderField as BaseField

class NestedField( BaseField ):

	@property
	def context( self ):
		if self._context is None:

			from . import SpiderFields

			syntax = self.syntax
			value = self.value
			rvalue = value[ "value" ]

			field = SpiderFields.by_value( rvalue )

			context = {}
			for row in self.selector( self.key[1:] ):
				context.update( field( selector = getattr( row, syntax ), **value ).context )

			self._context = context
		return self._context
