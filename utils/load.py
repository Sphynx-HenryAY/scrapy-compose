
from functools import lru_cache

@lru_cache( maxsize = 64 )
def config( spider_name ):

	import yaml

	try:
		with open( f"{spider_name.replace('.','/')}.yml", "r" ) as config_f:
			return yaml.safe_load( config_f )
	except FileNotFoundError:
		return None

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
		module = import_module( f".{mod_name}", pkg_name )

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
		naming = f"{module.split('.',1)[0]}.{{spider.name}}"

	from inspect import isclass
	from scrapy import Spider
	from scrapy_compose.utils.load import package as load_package

	spiders = load_package( module, key = lambda s: (
		isclass( s ) and
		issubclass( s, Spider ) and
		getattr( s, "name", None )
	) )

	for s_name, spider in spiders.items():
		spider.name = naming.format( **locals() )
		namespace[ s_name ] = spider

	return namespace
