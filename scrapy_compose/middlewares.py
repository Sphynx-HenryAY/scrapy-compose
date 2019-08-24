
from scrapy import signals


class ScrapyComposeMiddleware(object):
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the spider middleware does not modify the
	# passed objects.

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_spider_input(self, response, spider):
		# Called for each response that goes through the spider
		# middleware and into the spider.

		# Should return None or raise an exception.
		return None

	def process_spider_output(self, response, result, spider):
		# Called with the results returned from the Spider, after
		# it has processed the response.

		# Must return an iterable of Request, dict or Item objects.

		from scrapy import Item

		from scrapy_compose import output
		from scrapy_compose.load import config as load_config
		from scrapy_compose.items import DynamicItem

		config = ( load_config( spider.__module__ ) or {} ).get( "output", {} )

		if not config:
			for i in result:
				yield i
			return

		spider_name = spider.__module__

		for i in result:
			if isinstance( i, Item ):
				yield DynamicItem(
					**output( i, config = config )
				)
			else:
				yield i

	def process_spider_exception(self, response, exception, spider):
		# Called when a spider or process_spider_input() method
		# (from other spider middleware) raises an exception.

		# Should return either None or an iterable of Response, dict
		# or Item objects.
		pass

	def process_start_requests(self, start_requests, spider):
		# Called with the start requests of the spider, and works
		# similarly to the process_spider_output() method, except
		# that it doesn’t have a response associated.

		# Must return only requests (not items).
		for r in start_requests:
			yield r

	def spider_opened(self, spider):
		if not hasattr( spider.__class__, "spider-config" ):
			from scrapy_compose import compose
			from scrapy_compose.load import config as load_config

			spider_name = spider.__module__

			config = load_config( spider_name ) or {}
			parsers = config.get( "parsers", {} )

			if parsers:

				for pname in parsers:
					p_func = getattr( spider.__class__, pname, None )

					if not p_func:
						def p_func( self, response ): pass
						p_func.__name__ = pname

					setattr( spider.__class__, pname, compose( p_func ) )

			setattr( spider.__class__, "spider-config", config )
			spider.logger.info( '%s with spider-compose initialized' % spider.name )

		spider.logger.info('Spider opened: %s' % spider.name)

