
from abc import ABC as AbstractClass
from collections import defaultdict, namedtuple

from .alternating_field import AlternatingField
from .matryoshka_field import MatryoshkaField
from .nested_field import NestedField
from .string_field import StringField
from .tablize_field import TablizeField

from ..utils import Utils

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
		_type = namedtuple(
			type_name,
			"field key",
			defaults = ( field, key )
		)
		setattr( cls, type_name, _type )
		return _type

class Fields:

	for cname, field in globals().items():

		if (
				cname.endswith( "Field" ) and
				AbstractClass not in field.__bases__
			):
			vars()[ cname ] = field
			Types.register( field )

	else:
		del cname, field

	@classmethod
	def register( cls, field ):
		from .field import Field
		if Field in field.__bases__:
			setattr( cls, field.__name__, field )
			Types.register( field )
		else:
			raise TypeError( f"{field} is not {Field}" )
		return field

	@classmethod
	def by_key( cls, parse_type ):
		return Types.by_key( parse_type ).field

	@classmethod
	def by_value( cls, value ):
		return Types.by_value( value ).field

