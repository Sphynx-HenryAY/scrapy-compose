
from ..utils import realize
from .field import Field

class StringField( Field ):

	def __init__( self, key = None, value = None, selector = None ):
		#unify value format
		if isinstance( value, str ):
			value = {
				"_type": "string",
				"value": value
			}
		super().__init__( key = key, value = value, selector = selector )

	@property
	def content( self ):
		if self._content is None:

			selector = self.selector

			self._content = {
				realize( selector, self.key ): realize( selector, self.value[ "value" ] )
			}

		return self._content
