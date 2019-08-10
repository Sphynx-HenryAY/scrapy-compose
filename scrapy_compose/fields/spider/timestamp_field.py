
from scrapy_compose.utils import realize
from .fields import SpiderField as BaseField

class TimestampField( BaseField ):

	default_format = "%Y-%m-%dT%H:%M:%S%z"

	@property
	def context( self ):
		if not self._context:
			from datetime import datetime
			if self.value and "format" in self.value:
				t_format = self.value[ "format" ]
			else:
				t_format = self.default_format
			self._context = { realize( self.selector, self.key ): datetime.utcnow().strftime( t_format ) }
		return self._context
