from scrapy.commands.crawl import Command as BaseCommand

class Command( BaseCommand ):

	def syntax( self ):
		return "[options] <pattern>"

	def short_desc( self ):
		return "Run spiders with name matched with pattern."
