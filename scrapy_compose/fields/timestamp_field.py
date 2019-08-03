
from ..utils import realize
from .field import Field

class TimestampField( Field ):

	default_format = "%Y-%m-%dT%H:%M:%S%z"

	@property
	def content( self ):
		if not self._content:
			from datetime import datetime
			if self.value and "format" in self.value:
				t_format = self.value[ "format" ]
			else:
				t_format = self.default_format
			self._content = { realize( self.selector, self.key ): datetime.utcnow().strftime( t_format ) }
		return self._content
