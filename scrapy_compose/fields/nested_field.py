
from ..sanitizers import concreted
from .field import Field

class NestedField( Field ):

	@property
	def content( self ):
		if self._content is None:

			syntax = self.syntax
			value = self.value
			rkey, rvalue = value[ "key" ], value[ "value" ]

			from . import Fields
			field = Fields.by_value( rvalue )

			context = {}
			for row in self.selector( self.key[1:] ):
				context.update(
					field(
						key = rkey,
						value = rvalue,
						selector = getattr( row, syntax )
					).content
				)

			self._content = context
		return self._content
