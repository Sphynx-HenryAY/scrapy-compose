
from scrapy_compose.utils import tablize, realize

from ..base import FuncField
from .fields import SpiderField as BaseField

class TablizeField( FuncField, BaseField ):

	func = tablize

	def make_field( self, selector, _type = None, key = None, **kwargs ):
		syntax = selector.__name__
		kwargs[ "table" ] = getattr( selector( kwargs[ "table" ] ), syntax )
		return { realize( selector, key ): self.func( **kwargs ) }
