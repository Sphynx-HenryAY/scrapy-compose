
def compose( func ):

	def func_wrapper( self, response, *args, **kwargs ):
		p_name = func.__name__

		if not hasattr( self, "parsers" ):
			from scrapy_compose.fields.compose import ParserCompose
			from scrapy_compose.utils.load import config as load_config

			s_config = load_config( self.__module__ )
			p_config = ( s_config
				.get( "parsers", {} )
				.get( p_name, {} )
			)

			if not p_config:
				return func( self, response )

			parser = ParserCompose(
				key = p_name,
				value = p_config,
				syntax = s_config.get( "syntax", None ),
				spider = self,
			)
		else:
			parser = self.parsers[ p_name ]

		if parser.has_endpoints:
			return parser( response )

		response.meta[ "compose" ] = parser.get_context( response )

		return func( self, response, *args, **kwargs )

	return func_wrapper

class Output:

	cache = {}

	def __init__( self, spider = None ):

		if spider:
			self._cache( spider )

	def _cache( self, spider ):

		s_cls = spider.__class__

		if s_cls in self.cache:
			return self.cache[ s_cls ]

		from scrapy_compose.utils.load import config as load_config
		output = load_config( spider.__module__ ).get( "output", {} )

		if not output:
			return

		from collections import defaultdict

		keys = output.get( "keys", {} )
		if isinstance( keys, list ):
			keys = { k: k for k in keys }

		active_filter = output.get( "filter", False )
		exclude = set( output.get( "exclude", [] ) )
		if active_filter:
			exclude |= spider_item.keys() - keys.keys()

		self.cache[ s_cls ] = {
			"keys": keys,
			"exclude": exclude,
			"values": output.get( "values", defaultdict( dict ) )
		}

		return self.cache[ s_cls ]

	def process( self, spider, item ):

		config = self.cache.get( spider.__class__, None )
		if config is None:
			return item

		keys = config[ "keys" ]
		values = config[ "values" ]
		exclude = config[ "exclude" ]

		context = {}

		for k, v in item.items():

			if k in exclude:
				continue

			final_k = keys.get( k, k )
			if final_k in values:
				d_val = values[ final_k ]
				v = d_val.get( v, d_val.get( "default", v ) )

			context[ final_k ] = v

		return context

	def __call__( self, func ):
		from scrapy_compose.items import DynamicItem
		process = self.process

		def func_wrapper( spider, response ):

			self._cache( spider )

			for item in func( spider, response ):
				yield DynamicItem( **process( spider, item ) )

		return func_wrapper
