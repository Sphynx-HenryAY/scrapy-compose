
from scrapy_compose.utils.context import tablize, realize

from .field import FuncField as BaseField

class TablizeField( BaseField ):

	def make_field( self, selector, _type = None, key = None, **kwargs ):
		syntax = selector.__name__
		kwargs[ "table" ] = getattr( selector( kwargs[ "table" ] ), syntax )
		return { realize( selector, key ): tablize( **kwargs ) }
