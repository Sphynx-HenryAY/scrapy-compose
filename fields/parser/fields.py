from ..base import Fields
from .field import ParserField

class ParserTypes( Fields.Types ): pass

class ParserFields( Fields ):
	Field = ParserField
	Types = ParserTypes
