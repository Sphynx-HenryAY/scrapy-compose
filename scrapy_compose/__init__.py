from . import fields, utils, sanitizers, load

def compose( func ):

	def func_wrapper( self, response, *args, **kwargs ):
		fname = func.__name__

		if hasattr( self.__class__, "spider-config" ):
			spider_config = getattr( self.__class__, "spider-config" )
		else:
			spider_config = load.config( func.__module__ )

		if spider_config is None or fname not in spider_config:
			return func( self, response )

		from .fields import Fields

		f_config = spider_config[ fname ]
		selector = getattr( response, spider_config.get( "selector", "css" ) )

		item = f_config.pop( "_item", {} )

		context = {}

		for k, v in f_config.items():
			field = Fields.by_value( v )
			context.update( field( k, v, selector ).content )

		if item:
			return load.resource( item )( **context )

		response.meta[ "compose" ] = context

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
