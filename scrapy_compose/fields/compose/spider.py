
from .fields import ComposeField

class SpiderCompose( ComposeField ):

	support_ext = [ "yml", "yaml", "json" ]
	_composed = None

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
					import_module( pkg_name + "." + f_name )
					continue

				except ModuleNotFoundError:
					namespace[ f_name ] = (
						cls(
							key = f_name,
							value = yaml.safe_load( open( f ) )
						)
					)

		return namespace

	def __init__( self, key = None, value = None, model = None, **kwargs ):

		if model is None:
			from scrapy import Spider as model

		self.model = model
		value.update( getattr( model, "config", {} ) )

		if key is None:
			from scrapy_compose.utils import genuid
			key = genuid()

		super( SpiderCompose, self ).__init__( key = key, value = value, **kwargs )

	@property
	def composed( self ):
		if not self._composed:
			self._composed = self._Compose(
				s_name = self.key,
				s_config = self.value,
				base_spidercls = self.model
			)
		return self._composed

	@staticmethod
	def _Compose( s_name = None, s_config = None, base_spidercls = None ):

		if not s_config:
			return base_spidercls

		from scrapy import Spider as BaseSpider

		from scrapy_compose.decorators import compose
		from scrapy_compose.compose_settings import DEFAULT_SYNTAX
		from scrapy_compose.fields import ComposeFields

		ParserCompose = ComposeFields.ParserCompose

		base_parse = BaseSpider.parse
		syntax = s_config.get( "syntax", DEFAULT_SYNTAX )

		class spidercls( base_spidercls ):

			name = s_name
			config = s_config

			parsers = {}

			# name can be overwritten by config
			for k, v in config.items():
				if k not in ComposeFields.fields:
					vars()[ k ] = v

			for p_name, p_config in config.get( ParserCompose.fkey, {} ).items():
				parser = getattr( base_spidercls, p_name, None )

				if parser and parser is not base_parse:
					parser = compose( parser )

				else:
					parser = ParserCompose(
						key = p_name,
						value = p_config,
						syntax = syntax
					)
					parsers[ p_name ] = parser

				vars()[ p_name ] = parser

			def __init__( self, *args, **kwargs ):

				for p_name, parser in self.parsers.items():
					parser.spider = self
					setattr( self, p_name, parser )

				super( base_spidercls, self ).__init__( *args, **kwargs )

		return spidercls
