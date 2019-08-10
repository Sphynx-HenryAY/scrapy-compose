
from scrapy_compose.utils import realize

from ..base import FuncField
from .fields import SpiderField as BaseField

class StringField( FuncField, BaseField ):

	func = realize

	def __init__( self, key = None, value = None, selector = None, **kwargs ):
		#unify value format
		if isinstance( value, str ):
			value = { "_type": "string", "value": value }
		super().__init__( key = key, value = value, selector = selector, **kwargs )

	def make_field( self, selector, key = None, value = None, **kwargs ):
		return { realize( selector, key ): self.func( selector, value ) }
