
from .fields import ComposeField

class SpiderCompose( ComposeField ):

	from .parser import ParserCompose

	name = None
	support_ext = [ "yml", "yaml", "json" ]
	fields = {
		"parsers": ParserCompose
	}

	@classmethod
	def from_package( cls, pkg_name, namespace = None ):

		if namespace is None:
			namespace = {}

		import yaml
		import glob
		from importlib import import_module
		from os.path import join, dirname as get_dirname

		dirname = get_dirname( import_module( pkg_name ).__file__ )
		support_ext = cls.support_ext

		for f in glob.glob( join( dirname, "*" ) ):

			f_path, _, f_ext = f.rpartition( "." )
			f_name = f_path.rpartition( "/" )[-1]

			if f_ext in support_ext and f_name not in namespace:

				try:
					import_module( f"{pkg_name}.{f_name}" )
					continue

				except ModuleNotFoundError:
					namespace[ f_name ] = (
						cls(
							key = f_name,
							value = yaml.safe_load( open( f ) )
						)
						.composed
					)

		return namespace

	def __init__( self, key = None, value = None, **kwargs ):
		super().__init__( key = key, value = value, **kwargs )
		value = self.value

		from scrapy import Spider
		class spidercls( Spider ):

			from collections import defaultdict
			from scrapy_compose.utils import genuid

			name = key if key is not None else genuid()
			compose = self.compose
			composed = defaultdict( dict )

			for k in set( self.fields ) & set( value ):
				for f_name, field in compose( k ).items():
					vars()[ f_name ] = field
					composed[ k ][ f_name ] = field

			for attr in set( value ):
				vars()[ attr ] = value[ attr ]

			def __init__( spider, *args, **kwargs ):
				super().__init__( *args, **kwargs )
				spider.composed[ "spider" ] = spider
				for parser in spider.composed[ "parsers" ].values():
					parser.spider = spider

		self.composed = spidercls

	def compose( self, compose_key, namespace = None ):

		if namespace is None:
			namespace = {}

		from scrapy_compose.compose_settings import DEFAULT_SYNTAX

		composed = self.composed
		Field = self.fields[ compose_key ]
		value = self.value

		for f_name, f_config in value.pop( compose_key, {} ).items():
			namespace[ f_name ] = Field(
				key = f_name,
				value = f_config,
				syntax = value.get( "syntax", DEFAULT_SYNTAX )
			)

		return namespace
