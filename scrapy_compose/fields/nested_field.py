
from ..utils import Utils
from .field import Field

class NestedField( Field ):

	@property
	def content( self ):
		if self._content is None:
			self._content = self._init_content( init = True )
		return self._content

	def _init_content( self, init = False,
			context = None,
			rows = None,
			value = None,
		):

		if context is None:
			context = {}
			rows = self.selector( self.key[1:] )
			value = self.value

		stripped = Utils.stripped
		def xtrt( sel, q ):
			return " ".join( stripped( sel( q ).extract() ) )

		rkey, rvalue = value[ "key" ], value[ "value" ]
		syntax = self.syntax

		for row in rows:
			sel = getattr( row, syntax )
			if isinstance( rvalue, dict ):
				from . import Fields
				field = Fields.by_value( rvalue )
				context.update(
					field( key = rkey, value = rvalue, selector = sel ).content
				)
			else:
				context[ xtrt( sel, rkey[1:] ) ] = xtrt( sel, rvalue[1:] )

		return context
