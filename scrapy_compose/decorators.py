
from . import compose_settings

from scrapy_compose.fields.compose import ParserCompose
from scrapy_compose.utils.load import config as load_config

def compose( func ):

	def func_wrapper( self, response, *args, **kwargs ):
		pname = func.__name__

		if hasattr( self.__class__, "config" ):
			spider_config = getattr( self.__class__, "config" )
		else:
			spider_config = load_config( func.__module__ )

		if spider_config is None:
			return func( self, response )

		p_config = ( spider_config
			.get( "parsers", {} )
			.get( pname, {} )
		)

		if not p_config:
			return func( self, response )

		syntax = spider_config.get( "syntax", compose_settings.DEFAULT_SYNTAX )

		parser = ParserCompose(
			key = pname,
			value = p_config,
			syntax = syntax,
			spider = self,
		)

		if parser.has_endpoints:
			return parser( response )

		response.meta[ "compose" ] = parser.get_context( response )

		return func( self, response, *args, **kwargs )

	return func_wrapper

def output( spider_item, config ):

	from collections import defaultdict

	keys = config.get( "keys", {} )
	if isinstance( keys, list ):
		keys = { k: k for k in keys }

	active_filter = config.get( "filter", False )
	exclude = set( config.get( "exclude", [] ) )
	if active_filter:
		exclude |= spider_item.keys() - keys.keys()

	context = {}
	values = config.get( "values", defaultdict( dict ) )

	for k, v in spider_item.items():

		if k in exclude:
			continue

		final_k = keys.get( k, k )
		if final_k in values:
			d_val = values[ final_k ]
			v = d_val.get( v, d_val.get( "default", None ) )

		context[ final_k ] = v

	return context
