from scrapy.spiderloader import SpiderLoader as BaseSpiderLoader

class SpiderLoader( BaseSpiderLoader ):

	def _load_all_spiders( self ):
		from .utils.load import spiders as load_spiders
		for name in self.spider_modules:
			self._spiders.update( {
				s.name: s
				for s in load_spiders( name ).values()
			} )
