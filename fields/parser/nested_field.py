
from .field import ParserField as BaseField

class NestedField( BaseField ):

	def get_context( self, response ):
		from . import ParserFields

		syntax = self.syntax
		value = self.value
		rvalue = value[ "value" ]

		field = ParserFields.from_config( **value )

		context = {}
		for row in self.get_selector( response )( self.key[1:] ):
			context.update( field.get_context( row ) )

		return context
