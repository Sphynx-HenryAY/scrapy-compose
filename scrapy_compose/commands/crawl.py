from scrapy.commands.crawl import Command as BaseCommand

class Command( BaseCommand ):

	def syntax( self ):
		return "[options] <pattern>"

	def short_desc( self ):
		return "Run spiders with name matched with pattern."

	def run( self, args, opts ):
		from scrapy_compose.utils.command import spider_filter

		s_list = spider_filter(
			self.crawler_process.spider_loader.list(),
			args.pop( 0 )
		)

		for s_name in s_list:
			self.crawler_process.crawl( s_name, **opts.spargs )

		self.crawler_process.start()
		if self.crawler_process.bootstrap_failed:
			self.exitcode = 1
