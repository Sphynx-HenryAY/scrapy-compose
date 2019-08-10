from . import fields, utils, sanitizers, load

DEFAULT_SYNTAX = "css"

def compose( func ):

	def func_wrapper( self, response, *args, **kwargs ):
		fname = func.__name__

		if hasattr( self.__class__, "spider-config" ):
			spider_config = getattr( self.__class__, "spider-config" )
		else:
			spider_config = load.config( func.__module__ )

		if spider_config is None or fname not in spider_config:
			return func( self, response )

		syntax = spider_config.get( "selector", DEFAULT_SYNTAX )

		cps = fields.compose.SpiderCompose(
			key = fname,
			value = spider_config[ fname ],
			selector = getattr( response, syntax )
		)

		if cps.is_endpoint:
			return cps.endpoint

		response.meta[ "compose" ] = cps.context

		return func( self, response, *args, **kwargs )

	return func_wrapper

def output( spider_name, spider_item, config = None ):

	if config is None:
		config = load.config( spider_name )

	filter_output = config.get( "output_filter", False )
	exclude = config.get( "output_exclude", [] )
	fields = config.get( "output", {} )

	for ex in exclude:
		fields.pop( ex, None )
		spider_item.pop( ex, None )

	if filter_output:
		return {
			fields[k]: v
			for k, v in spider_item.items()
			if k in fields
		}
	else:
		return {
			fields.get( k, k ): spider_item.get( k, "" )
			for k in set( fields )|set( spider_item )
		}
