from ..base import Fields

class ComposeField( Fields.Field ): pass

class ComposeTypes( Fields.Types ): pass

class ComposeFields( Fields ):
	Field = ComposeField
	Types = ComposeTypes
