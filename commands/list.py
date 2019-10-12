from scrapy.commands.list import Command as BaseCommand

class Command( BaseCommand ):

	def syntax( self ):
		return "[< spider name pattern >]"

	def run( self, args, opts ):

		s_list = self.crawler_process.spider_loader.list()
		if args:
			from scrapy_compose.utils.command import spider_filter
			s_list = spider_filter( s_list, args[0] )

		for s in sorted( s_list ):
			print( s )
