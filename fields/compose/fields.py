from ..base import Fields

class ComposeField( Fields.Field ):

	composed = None

	def __call__( self, *args, **kwargs ):
		return self.composed( *args, **kwargs )

class ComposeTypes( Fields.Types ): pass

class ComposeFields( Fields ):
	Field = ComposeField
	Types = ComposeTypes
