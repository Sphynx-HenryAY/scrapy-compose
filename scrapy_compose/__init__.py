from . import fields, utils, processors, compose_settings

__version__ = '0.8.3dev'

def compose( func ):

	def func_wrapper( self, response, *args, **kwargs ):
		pname = func.__name__

		if hasattr( self.__class__, "spider-config" ):
			spider_config = getattr( self.__class__, "spider-config" )
		else:
			spider_config = utils.load.config( func.__module__ )

		parsers = spider_config.get( "parsers", {} )

		if spider_config is None or pname not in parsers:
			return func( self, response )

		syntax = spider_config.get( "syntax", compose_settings.DEFAULT_SYNTAX )

		parser = fields.compose.ParserCompose(
			key = pname,
			value = parsers[ pname ],
			syntax = syntax,
		)

		if parser.has_endpoints:
			parser.spider = self
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
