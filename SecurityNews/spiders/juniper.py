# -*- coding: utf-8 -*-
import scrapy


class JuniperSpider(scrapy.Spider):
	name = 'juniper'
	allowed_domains = ['kb.juniper.net']
	start_urls = [
		"https://kb.juniper.net/InfoCenter/index?page=content&id=JSA10935&actp=METADATA",
		"http://kb.juniper.net/InfoCenter/index?page=content&id=JSA10684"
	]

	def parse(self, response):
		pass
