
from .fields import ComposeField

class SpiderCompose( ComposeField ):

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
		super().__init__( key = key, value = value, **kwargs )
		self.composed = self._Compose(
			s_name = self.key,
			s_config = self.value,
		)

	@staticmethod
	def _Compose( s_name = None, s_config = None, base_spidercls = None ):

		if s_name is None:
			from scrapy_compose.utils import genuid
			s_name = genuid()

		if s_config is None:
			s_config = {}

		if base_spidercls is None:
			from scrapy import Spider as base_spidercls

		class spidercls( base_spidercls ):

			from .fields import ComposeFields

			name = s_name

			for k, v in s_config.items():

				if k in ComposeFields.fields:
					Compose = ComposeFields.fields[ k ]
					for c_name, c_config in v.items():
						v[ c_name ] = Compose( key = c_name, value = c_config )

				vars()[ k ] = v

			def __init__( spider, *args, **kwargs ):
				from scrapy_compose.fields.compose import ParserCompose

				for p_name, parser in getattr( spider, ParserCompose.fkey ).items():
					parser.spider = spider
					setattr( spider, p_name, parser )

		return spidercls
