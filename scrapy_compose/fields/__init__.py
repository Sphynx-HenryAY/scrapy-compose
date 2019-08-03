
from .field import Field
from ..load import package as load_package

__all__ = [ "Field" ]

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

	@classmethod
	def register( cls, field ):
		if cls.registrable( field ):
			setattr( cls, field.__name__, field )
			Types.register( field )
			return field

	@staticmethod
	def registrable( field ):
		from inspect import isclass
		return isclass( field ) and field is not Field and issubclass( field, Field )

	@classmethod
	def by_key( cls, parse_type ):
		return Types.by_key( parse_type ).field

	@classmethod
	def by_value( cls, value ):
		return Types.by_value( value ).field

load_package( __name__, vars(), lambda c: Fields.register( c ) )
