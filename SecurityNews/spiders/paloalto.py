# -*- coding: utf-8 -*-

from itertools import zip_longest

import scrapy

from scrapy_compose.utils import Utils

from SecurityNews.spiders.base import TIPSpider
from SecurityNews.items import SecurityNewsItem

class PaloAltoSpider( TIPSpider ):
	name = "paloalto"
	start_urls = [ "https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000Cm68CAC" ]

	def merge_td( self, td ):
		return "".join( Utils.stripped( td.css( "*::text" ).extract() ) )

	def parse( self, response ):

		trs = response.css( "tr" )

		theads = [ self.merge_td( td ) for td in trs[0].css( "td" ) ]

		# header row has been popped
		for tr in trs[1:]:
			yield SecurityNewsItem.DynamicItem(
				**dict( zip(
					theads,
					( self.merge_td( td ) for td in tr.css( "td" ) )
				) )
			)
