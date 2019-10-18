from ..base import Fields

class ComposeField( Fields.Field ):

	from scrapy_compose.utils import classproperty

	suff_len = 7
	plural = "s"

	@classproperty
	def fkey( cls ):
		return cls.__name__[:-cls.suff_len].lower() + cls.plural

class ComposeFields( Fields ):
	Field = ComposeField
