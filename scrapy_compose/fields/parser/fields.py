from ..base import Fields
from .field import ParserField

class ParserFields( Fields ):
	Field = ParserField

	@classmethod
	def from_config( cls, config ):
		fkey = config[ "_type" ] if isinstance( config, dict ) else "string"
		return cls.fields[ fkey ]
