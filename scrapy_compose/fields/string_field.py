
from ..utils import realize
from .field import FuncField

class StringField( FuncField ):

	func = realize

	def __init__( self, key = None, value = None, selector = None ):
		#unify value format
		if isinstance( value, str ):
			value = { "_type": "string", "value": value }
		super().__init__( key = key, value = value, selector = selector )

	def make_field( self, selector, key = None, value = None, **kwargs ):
		return { realize( selector, key ): self.func( selector, value ) }
