# -*- coding: utf-8 -*-

from SecurityNews.spiders.base import TIPSpider

class TraceFfiveSpider( TIPSpider ):
	name = "ffive"
	allowed_domains = ["cdn.f5.com"]
	start_urls = [ "https://cdn.f5.com/product/bugtracker/" ]
