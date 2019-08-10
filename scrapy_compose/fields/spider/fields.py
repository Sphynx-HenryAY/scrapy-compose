from ..base import Fields

class SpiderField( Fields.Field ): pass

class SpiderTypes( Fields.Types ): pass

class SpiderFields( Fields ):
	Field = SpiderField
	Types = SpiderTypes
