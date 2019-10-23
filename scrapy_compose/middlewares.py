
from scrapy import signals


class ScrapyComposeMiddleware(object):
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the spider middleware does not modify the
	# passed objects.

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		spidercls = crawler.spidercls

		if not hasattr( spidercls, "spider-config" ):
			from scrapy import Spider as BaseSpider

			from scrapy_compose import compose
			from scrapy_compose.fields.compose.parser import ParserCompose
			from scrapy_compose.utils.load import config as load_config

			config = load_config( spidercls.__module__ ) or {}
			parsers = config.get( ParserCompose.fkey, {} )

			base_parse = BaseSpider.parse

			for pname, p_config in parsers.items():
				parser = getattr( spidercls, pname, None )

				if parser and parser is not base_parse:
					parser = compose( parser )

				else:
					parser = ParserCompose(
						key = pname,
						value = p_config,
					)
					parsers[ pname ] = parser

				setattr( spidercls, pname, parser )

			setattr( spidercls, ParserCompose.fkey, parsers )
			setattr( spidercls, "spider-config", config )

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
		from scrapy_compose.utils.load import config as load_config
		from scrapy_compose.items import DynamicItem

		config = ( load_config( spider.__module__ ) or {} ).get( "output", {} )

		if not config:
			for i in result:
				yield i
			return

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
		# that it doesn't have a response associated.

		# Must return only requests (not items).
		for r in start_requests:
			yield r

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)

		from scrapy_compose.fields.compose.parser import ParserCompose
		for p_name, parser in getattr( spider, ParserCompose.fkey ).items():
			if isinstance( parser, ParserCompose ):
				parser.spider = spider
