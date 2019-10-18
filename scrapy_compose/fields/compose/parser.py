
from .fields import ComposeField
from ..parser.fields import ParserFields, ParserField

class ParserCompose( ComposeField, ParserField ):

	_fields = None

	def __init__( self, spider = None, syntax = None, **kwargs ):
		super( ParserCompose, self ).__init__( **kwargs )

		from scrapy.utils.project import get_project_settings

		self.spider = spider
		self.composed = self.get_endpoints

		if syntax is not None:
			self.syntax = syntax
		else:
			from scrapy_compose.compose_settings import DEFAULT_SYNTAX
			self.syntax = self.meta.pop( "syntax", DEFAULT_SYNTAX )

	def get_context( self, response ):
		ctx = {}
		for field in self.fields:
			ctx.update( field.get_context( response ) )
		return ctx

	@property
	def fields( self ):
		if not self._fields:
			self._fields = [
				ParserFields.from_config( v )( key = k, value = v )
				for k, v in self.value.items()
			]
		return self._fields

	@property
	def has_endpoints( self ):
		return bool( self.meta )

	def get_endpoints( self, response ):

		if not self.has_endpoints:
			yield None
			return

		from scrapy import Request

		selector = self.get_selector( response )

		meta = self.meta
		spider = self.spider

		if "item" in meta:
			from scrapy_compose.utils.load import resource as load_resource
			yield load_resource( meta[ "item" ] )( **self.get_context( response ) )

		if "items" in meta:
			for query, callback in meta[ "items" ].items():
				f_callback = getattr( spider, callback )
				if query.startswith( "@" ):
					for block in selector( query[1:] ):
						yield next( f_callback( block ) )

		if "requests" in meta:
			for url_str, callback in meta[ "requests" ].items():
				f_callback = getattr( spider, callback )

				if url_str.startswith( "@" ):
					# realize will return string data directly if len( selected ) is 1
					urls = selector( url_str[1:] ).extract()
				else:
					urls = [ url_str ]

				for url in urls:
					yield Request( url, callback = f_callback )


		if "follows" in meta:
			from scrapy.utils.response import get_base_url
			from urllib.parse import urljoin

			base_url = get_base_url( response )
			for url_str, callback in meta[ "follows" ].items():
				f_callback = getattr( spider, callback )

				if url_str.startswith( "@" ):
					# realize will return string data directly if len( selected ) is 1
					urls = [ urljoin( base_url, url ) for url in selector( url_str[1:] ).extract() ]
				else:
					urls = [ urljoin( base_url, url_str ) ]

				for url in urls:
					yield Request( url, callback = f_callback )
