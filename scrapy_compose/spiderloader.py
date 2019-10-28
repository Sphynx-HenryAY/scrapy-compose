from scrapy.spiderloader import SpiderLoader as BaseSpiderLoader

class SpiderLoader( BaseSpiderLoader ):

	def _load_all_spiders( self ):
		from scrapy_compose.fields.compose.spider import SpiderCompose

		spiders = self._spiders

		for name in self.spider_modules:

			pkg_name = name.split( ".", 1 )[ 0 ]

			for s_name, s_compose in SpiderCompose.from_package( name ).items():

				spider = s_compose.composed
				spider.name = pkg_name + "." + spider.name

				spiders[ spider.name ] = spider
