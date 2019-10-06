
from .fields import ComposeField
from ..parser.fields import ParserFields, ParserField

class ParserCompose( ParserField, ComposeField ):

	def __init__( self, spider = None, **kwargs ):
		super().__init__( **kwargs )

		self.spider = spider

	def get_context( self, response ):

		ctx = {}
		for k, v in self.value.items():
			ctx.update( ParserFields.from_config( key = k, value = v )
				.get_context( response )
			)

		return ctx

	@property
	def has_endpoints( self ):
		return (
			"item" in self.meta or
			"items" in self.meta or
			"requests" in self.meta
		)

	def get_endpoints( self, response ):

		if not self.has_endpoints:
			return None

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
			from scrapy import Request

			for urls, callback in meta[ "requests" ].items():
				f_callback = getattr( spider, callback )

				if urls.startswith( "@" ):
					# realize will return string data directly if len( selected ) is 1
					urls = selector( urls[1:] ).extract()
				else:
					urls = [ urls ]

				for url in urls:
					yield Request( url, callback = f_callback )
