from ..base import Fields
from .field import ParserField

class ParserFields( Fields ):
	Field = ParserField

	class _PFfields( dict ):

		def __getitem__( self, config, default = "string" ):
			if isinstance( config, dict ):
				key = config.get( "_type", default )
			else:
				key = default
			return super( ParserFields._PFfields, self ).__getitem__( key )

	@Fields.classproperty
	def fields( cls ):
		if cls._fields is None:
			cls._fields = cls._PFfields()
		return cls._fields
