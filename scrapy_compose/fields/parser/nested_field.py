
from .field import ParserField as BaseField

class NestedField( BaseField ):

	@property
	def context( self ):
		if self._context is None:

			from . import ParserFields

			syntax = self.syntax
			value = self.value
			rvalue = value[ "value" ]

			field = ParserFields.from_config( **value )

			context = {}
			for row in self.selector( self.key[1:] ):
				context.update( field
					.reuse( selector = getattr( row, syntax ) )
					.context
				)

			self._context = context
		return self._context
