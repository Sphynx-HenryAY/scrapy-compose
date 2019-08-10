
from .fields import ComposeField
from ..spider.fields import SpiderFields

class SpiderCompose( ComposeField ):

	_endpoint = None

	def __init__( self, key = None, value = None, selector = None, **kwargs ):

		super().__init__( key = key, value = value, selector = selector, **kwargs )
		self.meta = value.get( "_meta", {} )

	@property
	def context( self ):
		if not self._context:

			selector = self.selector

			ctx = {}
			for k, v in self.value.items():

				if k == "_meta":
					continue

				ctx.update( SpiderFields.from_config( key = k, value = v, selector = selector ).context )

			self._context = ctx
		return self._context

	@property
	def is_endpoint( self ):
		return "item" in self.meta

	@property
	def endpoint( self ):

		if not self.is_endpoint:
			return None

		from scrapy_compose.load import resource as load_resource

		if not self._endpoint:
			self._endpoint = load_resource( self.meta[ "item" ] )( **self.context )

		return self._endpoint
