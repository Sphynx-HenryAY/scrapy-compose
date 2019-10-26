
try:
	from functools import lru_cache
except ImportError:
	from backports.functools_lru_cache import lru_cache

@lru_cache( maxsize = 64 )
def config( spider ):

	if hasattr( spider.__class__, "config" ):
		return spider.__class__.config

	import yaml

	try:
		with open( spider.__module__.replace('.','/') + ".yml", "r" ) as config_f:
			return yaml.safe_load( config_f )
	except FileNotFoundError:
		return {}

@lru_cache( maxsize = 64 )
def resource( path ):
	from importlib import import_module
	mod, func = path.rsplit( ".", 1 )
	return getattr( import_module( mod ), func )

def package( pkg_name, namespace = None, key = None ):

	from importlib import import_module
	from inspect import getmembers
	from os.path import basename, join, dirname as get_dirname
	import glob

	if key is None:
		key = lambda x: callable( x ) and not x.__name__.startswith( "__" )

	if namespace is None:
		namespace = {}

	pkg = import_module( pkg_name )

	dirname = get_dirname( pkg.__file__ )

	for mod_file_name in glob.glob( join( dirname, "*.py" ) ):

		if mod_file_name.endswith( "__init__.py" ):
			continue

		mod_name = basename( mod_file_name )[:-3]
		module = import_module( "." + mod_name, pkg_name )

		# if imported cls can be registered in Fields
		#	add it to local namespace
		for name, cls in getmembers( module, key ):
			namespace[ name ] = cls

		namespace.pop( mod_name, None )

	return namespace

def spiders( module, namespace = None, naming = None ):

	if namespace is None:
		namespace = {}

	if naming is None:
		naming = module.split('.',1)[0] + "." + "{spider.name}"

	from inspect import isclass
	from scrapy import Spider

	from scrapy_compose.fields.compose.spider import SpiderCompose

	spiders = package( module, key = lambda s: (
		isclass( s ) and
		issubclass( s, Spider ) and
		getattr( s, "name", None )
	) )
	SpiderCompose.from_package( module, spiders )

	for s_name, spider in spiders.items():

		if isinstance( spider, SpiderCompose ):
			spider = spider.composed
		else:
			spider = SpiderCompose._Compose(
				s_name = spider.name,
				s_config = config( spider ),
				base_spidercls = spider
			)

		spider.name = naming.format( **locals() )
		namespace[ s_name ] = spider

	return namespace

def settings( path ):
	from importlib import import_module
	module = import_module( path )

	return {
		k: getattr( module, k )
		for k in dir( module )
		if k.isupper()
	}
