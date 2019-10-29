
try:
	from functools import lru_cache
except ImportError:
	from backports.functools_lru_cache import lru_cache

@lru_cache( maxsize = 64 )
def config( module ):
	import yaml
	from os.path import exists
	from scrapy_compose.compose_settings import SUPPORT_EXTENSIONS

	file_path = module.replace('.','/')
	for ext in SUPPORT_EXTENSIONS:
		file_name = file_path + "." + ext
		if exists( file_name ):
			with open( file_name, "r" ) as f:
				return yaml.safe_load( f )

	return {}

@lru_cache( maxsize = 64 )
def resource( path ):
	from importlib import import_module
	mod, func = path.rsplit( ".", 1 )
	return getattr( import_module( mod ), func )

def pkg_files( pkg_name, pattern = "*" ):

	import glob
	from importlib import import_module
	from os.path import join, dirname as get_dirname

	return glob.glob( join(
		get_dirname( import_module( pkg_name ).__file__ ),
		pattern
	) )

def package( pkg_name, namespace = None, key = None ):

	from importlib import import_module
	from inspect import getmembers
	from os.path import basename

	if key is None:
		key = lambda x: callable( x ) and not x.__name__.startswith( "__" )

	if namespace is None:
		namespace = {}

	for mod_file_name in pkg_files( pkg_name, "*.py" ):

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
