
class Types:

	@classmethod
	def by_key( cls, key ):
		return getattr( cls, key.capitalize(), None )()

	@classmethod
	def by_value( cls, value ):
		field_type = (
			"string"
			if isinstance( value, str ) else
			value[ "_type" ]
		)
		return cls.by_key( field_type )

	@classmethod
	def register( cls, field ):

		key = field.__name__[:-5].lower()
		type_name = key.capitalize()

		if hasattr( cls, type_name ):
			return getattr( cls, type_name )

		from collections import namedtuple

		_type = namedtuple( type_name, "field key", defaults = ( field, key ) )
		setattr( cls, type_name, _type )

		return _type

class Fields:

	from .field import Field
	Field = Field
	Types = Types

	@classmethod
	def register( cls, field ):
		if cls.registrable( field ):
			setattr( cls, field.__name__, field )
			cls.Types.register( field )
			return field

	@classmethod
	def registrable( cls, field ):
		from inspect import isclass
		base_field = cls.Field
		return isclass( field ) and field is not base_field and issubclass( field, base_field )

	@classmethod
	def by_key( cls, parse_type ):
		return cls.Types.by_key( parse_type ).field

	@classmethod
	def by_value( cls, value ):
		return cls.Types.by_value( value ).field

	@classmethod
	def from_config( cls, config = None, **kwargs ):

		if config is None: config = {}
		config.update( kwargs )

		return cls.Types.by_value( config[ "value" ] ).field( **config )
