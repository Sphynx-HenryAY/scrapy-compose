
from .fields import ComposeField
from ..parser.fields import ParserFields, ParserField

class ParserCompose( ParserField, ComposeField ):

	def __init__( self, key = None, value = None, selector = None, spider = None, **kwargs ):
		super().__init__( key = key, value = value, selector = selector, **kwargs )

		self.spider = spider

	@property
	def context( self ):
		if not self._context:

			selector = self.selector

			ctx = {}
			for k, v in self.value.items():

				ctx.update( ParserFields.from_config( key = k, value = v, selector = selector ).context )

			self._context = ctx
		return self._context

	@property
	def has_endpoints( self ):
		return (
			"item" in self.meta or
			"items" in self.meta or
			"requests" in self.meta
		)

	@property
	def endpoints( self ):

		if not self.has_endpoints:
			return None

		meta = self.meta
		spider = self.spider
		selector = self.selector

		if "item" in meta:
			from scrapy_compose.load import resource as load_resource
			yield load_resource( meta[ "item" ] )( **self.context )

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
					urls = selector( urls[1:] ).extract()
				else:
					urls = [ urls ]

				for url in urls:
					yield Request( url, callback = f_callback )
