
from .field import ParserField as BaseField
from scrapy_compose.utils.context import realize

class JsonField( BaseField ):

	process_timing = [ "post_pack" ]

	def get_context( self, response ):
		selector = self.get_selector( response )

		from json import loads as json_loads

		j_selector = self.dict_selector( json_loads(
			realize( selector, self.value[ "json" ] )
		) )

		key = realize( selector, self.key )
		value = self.post_pack(
			realize( j_selector, self.value[ "query" ] )
		)

		return { key: value }

	def dict_selector( self, d_data ):

		from xml.etree.ElementTree import Element
		from scrapy import Selector
		from dict2xml import dict2xml

		return getattr(
			Selector( text = dict2xml( { "data": d_data } ) ),
			self.syntax
		)

