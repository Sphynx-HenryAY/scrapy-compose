# -*- coding: utf-8 -*-
import scrapy


class ThreatpostSpider(scrapy.Spider):
	name = 'threatpost'
	allowed_domains = ['threatpost.com']
	start_urls = ['https://threatpost.com/category/vulnerabilities/']

	def parse(self, response):
		pass
