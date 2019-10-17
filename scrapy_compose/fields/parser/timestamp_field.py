
from .field import ParserField as BaseField

class TimestampField( BaseField ):

	process_timing = [ "pre_pack" ]

	def get_context( self, response ):
		from datetime import datetime
		from scrapy_compose.utils.context import realize

		selector = self.get_selector( response )

		config = self.value

		if config and "value" in config and "from" in config:
			t_string = self.pre_pack( realize( selector, config[ "value" ] ) )
			t_stamp = datetime.strptime( t_string, config[ "from" ] )

		else:
			t_stamp = datetime.utcnow()

		return { realize( selector, self.key ): t_stamp }
