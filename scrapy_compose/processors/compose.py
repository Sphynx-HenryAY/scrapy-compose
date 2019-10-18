
from inspect import isclass

from scrapy.loader.processors import Compose

from scrapy_compose.utils.load import resource as load_resource


class Processor:

	def __init__( self, config = None ):

		s_parm = {}

		if not config:
			def s_proc( x ):
				return x

		elif isinstance( config, str ):
			s_proc = load_resource( config )

		elif isinstance( config, dict ):
			s_path, s_parm = next( iter( config.items() ) )
			s_proc = load_resource( s_path )

		if isclass( s_proc ):
			s_proc = s_proc( **s_parm )

		self.proc = s_proc

	def __call__( self, *args, **kwargs ):
		return self.proc( *args, **kwargs )


class ProcessorCompose( Compose ):

	def __init__( self, configs = None, *functions, **default_loader_context ):

		if isinstance( configs, list ):
			s_procs = [ Processor( config ) for config in configs ]
		else:
			s_procs = [ Processor( configs ) ]

		functions = list( functions ) + s_procs
		super( ProcessorCompose, self ).__init__( *functions, **default_loader_context )
