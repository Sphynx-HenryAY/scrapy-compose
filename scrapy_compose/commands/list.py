from scrapy.commands.list import Command as BaseCommand

class Command( BaseCommand ):

	def syntax( self ):
		return "[<pattern]"

	def short_desc( self ):
		return "List available spiders matched with pattern if provided."

	def add_options( self, parser ):
		super( Command, self ).add_options( parser )
		parser.add_option( "-c", "--count", dest = "count", action = "store_true", default = False )

	def run( self, args, opts ):

		s_list = self.crawler_process.spider_loader.list()
		if args:
			from scrapy_compose.utils.command import spider_filter
			s_list = spider_filter( s_list, args[0] )

		if opts.count:
			print( len( s_list ), "spiders matched." )
			return

		for s in sorted( s_list ):
			print( s )
