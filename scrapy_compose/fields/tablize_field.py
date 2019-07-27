
from ..utils import Utils
from .field import FuncField

class TablizeField( FuncField ):

	func = Utils.tablize

	def make_field( self, selector, _type = None, key = None, **kwargs ):
		syntax = selector.__name__
		kwargs[ "table" ] = getattr( selector( kwargs[ "table" ] ), syntax )
		return { Utils.realize( selector, key ): self.func( **kwargs ) }
