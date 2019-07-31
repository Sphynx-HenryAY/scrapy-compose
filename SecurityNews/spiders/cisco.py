# -*- coding: utf-8 -*-

from collections import defaultdict

import scrapy

from SecurityNews.spiders.base import TIPSpider
from SecurityNews.items import SecurityNewsItem

from scrapy_compose.fields import Fields
from scrapy_compose.utils import realize, tablize

class CiscoSpider( TIPSpider ):
	name = 'cisco'
	allowed_domains = [ 'tools.cisco.com' ]

	# for testing and development, handle later
	start_urls = {
		'https://tools.cisco.com/security/center/viewAlert.x?alertId=60384': False,
		'https://tools.cisco.com/security/center/viewAlert.x?alertId=60428': False,
		'https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-20190703-cucm-dos': True,
		'https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-20190515-nxos-cmdinj-1783': True,
	}

	def start_requests( self ):
		parsers = [ self.parse_non_cisco, self.parse_cisco ]
		for url, is_cisco in self.start_urls.items():
			yield scrapy.Request( url, callback = parsers[ is_cisco ], meta = { "is_cisco": is_cisco } )

	def parse_cisco( self, response ):
		context = defaultdict( list )
		context.update( response.meta.get( "compose", {} ) )
		context[ "is_cisco" ] = response.meta[ "is_cisco" ]

		def xtring( sel_list ):
			return [ x.strip() for x in sel_list.xpath( "string()" ).extract() ]

		title_node = None
		for i, ele in enumerate( response.css(
				f".ud-main-link-list:nth-child(1)>h2,"
				f".ud-main-link-list:nth-child(1)>ul table"
			) ):
			if ele.root.tag == "h2":
				title_node = ele
			elif ele.root.tag == "table":
				title = realize( title_node.css, "@.hbuttonelement ::text" )

				context[ title ].extend( tablize(
					table = ele.css,
					thead = [
						" ".join( x.split() )
						for x in xtring( ele.css( "thead th" ) )
					],
					qrows = "tbody tr",
					qrow = "td",
					row_process = xtring
				) )

		for table in response.css( ".ud-main-link-list:nth-child(1)>ul table" ):
			table.root.getparent().remove( table.root )

		context.update( Fields.AlternatingField(
			selector = response.css,
			key = (
				f"@.ud-main-link-list:nth-child(1)>h2:contains('Affected Products'),"
				f".ud-main-link-list:nth-child(1)>ul"
			),
			value = {
				"key": "@.hbuttonelement",
				"value": "@.ud-innercontent-area",
				"packing": "scrapy_compose.sanitizers.strip",
			}
		).content )

		yield SecurityNewsItem.DynamicItem( **context )

	def parse_non_cisco(self, response):
		context = response.meta.get( "compose", {} ) 
		context[ "is_cisco" ] = response.meta[ "is_cisco" ]
		yield SecurityNewsItem.DynamicItem( **context )
