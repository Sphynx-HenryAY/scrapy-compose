# -*- coding: utf-8 -*-

import scrapy

from scrapy_compose.items import DynamicItem

from SecurityNews.spiders.base import TIPSpider

class FfiveSpider( TIPSpider ):
	name = "ffive"
	allowed_domains = ["cdn.f5.com"]
	start_urls = [ "https://cdn.f5.com/product/bugtracker/" ]

	def parse_bug_content( self, response ):

		context = response.meta[ "compose" ]

		context[ "id" ] = context[ "id" ].split()[-1]

		# handle multiple article IDs
		articles = response.css( ".date-container a::text" ).extract()
		if len( articles ) > 1:
			context[ "Related AskF5 Article:" ] = ", ".join( articles )
			context.pop( ",", None )

		yield DynamicItem( **context )

