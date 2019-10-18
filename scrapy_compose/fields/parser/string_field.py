
from scrapy_compose.utils.context import realize
from .field import FuncField as BaseField

class StringField( BaseField ):

	process_timing = [ "post_pack" ]

	def __init__( self, key = None, value = None, selector = None, **kwargs ):
		#unify value format
		if isinstance( value, str ):
			value = { "_type": "string", "value": value }
		super( StringField, self ).__init__( key = key, value = value, selector = selector, **kwargs )

	def make_field( self, selector, key = None, value = None, **kwargs ):
		return { realize( selector, key ): self.post_pack( realize( selector, value ) ) }
