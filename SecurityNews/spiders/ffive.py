# -*- coding: utf-8 -*-

import scrapy

from SecurityNews.spiders.base import TIPSpider
from SecurityNews.items import SecurityNewsItem

class FfiveSpider( TIPSpider ):
	name = "ffive"
	allowed_domains = ["cdn.f5.com"]
	start_urls = [ "https://cdn.f5.com/product/bugtracker/" ]

	def start_requests( self ):
		for url in self.start_urls:
			yield scrapy.Request( url, callback = self.parse_bug_urls )

	def parse_bug_urls( self, response ):

		# record bugs listing page sequence
		from datetime import datetime
		yield { "timestamp": datetime.utcnow().strftime( "%Y-%m-%dT%H:%M:%S%z" ) }
		#yield { "bug_list": response.css( "a::text" ).extract() }

		for i, bug_url in enumerate( response.css( "a::attr(href)" ).extract() ):
			yield scrapy.Request( bug_url, callback = self.parse_bug_content, meta = { "order": i } )

	def parse_bug_content( self, response ):

		context = response.meta[ "compose" ]

		context[ "order" ] = response.meta[ "order" ]

		context[ "id" ] = context[ "id" ].split()[-1]

		# handle multiple article IDs
		articles = response.css( ".date-container a::text" ).extract()
		if len( articles ) > 1:
			context[ "Related AskF5 Article:" ] = ", ".join( articles )
			context.pop( ",", None )

		yield SecurityNewsItem.DynamicItem( **{
			k[:-1] if k.endswith( ":" ) else k: v
			for k, v in context.items()
		} )

