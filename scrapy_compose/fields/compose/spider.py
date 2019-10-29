
from .fields import ComposeField
from scrapy import Spider as BaseSpider


class SpiderCompose( ComposeField ):

	support_ext = [ "yml", "yaml", "json" ]
	_composed = None

	@classmethod
	def from_package( cls, pkg_name, namespace = None ):

		if namespace is None:
			namespace = {}

		import yaml
		from os.path import basename
		from inspect import isclass
		from scrapy_compose.utils.load import (
			pkg_files as load_pkg_files,
			package as load_package,
			config as load_config,
		)

		load_package( pkg_name, key = lambda s: (
			isclass( s ) and
			issubclass( s, BaseSpider ) and
			getattr( s, "name", None ) and
			namespace.update( { s.name: cls(
				key = s.name,
				value = load_config( s.__module__ ),
				model = s,
		) } ) ) )

		for ext in cls.support_ext:
			for f in load_pkg_files( pkg_name, "*." + ext ):

				f_name = basename( f ).rpartition( "." )[0]

				if f_name not in namespace:
					namespace[ f_name ] = cls(
						key = f_name,
						value = load_config( pkg_name + "." + f_name )
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
				p_composed = ParserCompose(
					key = p_name,
					value = p_config,
					syntax = syntax
				)

				if parser and parser is not base_parse:
					parser = compose( parser )
				else:
					parser = p_composed

				parsers[ p_name ] = p_composed
				vars()[ p_name ] = parser

			def __init__( self, *args, **kwargs ):

				for p_name, parser in self.parsers.items():
					parser.spider = self

				super( base_spidercls, self ).__init__( *args, **kwargs )

		return spidercls
