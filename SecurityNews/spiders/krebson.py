# -*- coding: utf-8 -*-
import scrapy


class KrebsonSpider(scrapy.Spider):
    name = 'krebson'
    allowed_domains = ['krebsonsecurity.com']
    start_urls = ['http://krebsonsecurity.com/']

    def parse(self, response):
        pass
