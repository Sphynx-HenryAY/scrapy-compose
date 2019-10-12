from ..base import Fields

class ComposeField( Fields.Field ):

	_composed = None

	def get_composed( self, *args, **kwargs ):
		pass

	def __call__( self, *args, **kwargs ):
		return self.get_composed( *args, **kwargs )

class ComposeTypes( Fields.Types ): pass

class ComposeFields( Fields ):
	Field = ComposeField
	Types = ComposeTypes
