
from .fields import ComposeField

class SpiderCompose( ComposeField ):

	name = None

	support_ext = [ "yml", "yaml", "json" ]

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

		from scrapy import Spider
		class spidercls( Spider ):

			from collections import defaultdict
			from scrapy_compose.compose_settings import DEFAULT_SYNTAX
			from scrapy_compose.utils import genuid
			from .parser import ParserCompose

			name = key if key is not None else genuid()
			compose = defaultdict( dict )

			for p_name, p_config in value.pop( "parsers", {} ).items():
				parser = ParserCompose(
					key = p_name,
					value = p_config,
					syntax = value.get( "syntax", DEFAULT_SYNTAX ),
				)
				vars()[ p_name ]  = parser
				compose[ "parser" ][ p_name ] = parser

			for attr in set( value ):
				vars()[ attr ] = value[ attr ]

			def __init__( self, *args, **kwargs ):
				super().__init__( *args, **kwargs )
				self.compose[ "spider" ] = self
				for parser in self.compose[ "parser" ].values():
					parser.spider = self

		self.composed = spidercls
