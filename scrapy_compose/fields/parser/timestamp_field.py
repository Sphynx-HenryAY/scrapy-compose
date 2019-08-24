
from .field import ParserField as BaseField

class TimestampField( BaseField ):

	default_format = "%Y-%m-%dT%H:%M:%S%z"

	@property
	def context( self ):
		if not self._context:
			from datetime import datetime
			from scrapy_compose.utils.context import realize

			selector = self.selector

			if self.value:

				config = self.value
				if "value" in config and "from" in config:
					t_value = datetime.strptime(
						realize( selector, config[ "value" ] ),
						config[ "from" ]
					)
				else:
					t_value = datetime.utcnow()

				t_stamp = t_value.strftime( config.get( "format", self.default_format ) )

			else:
				t_stamp = datetime.utcnow()

			self._context = { realize( selector, self.key ): t_stamp }
		return self._context
