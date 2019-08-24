# -*- coding: utf-8 -*-
import scrapy


class SecurelistSpider(scrapy.Spider):
    name = 'securelist'
    allowed_domains = ['securelist.com']
    start_urls = ['http://securelist.com/all/']

    def parse(self, response):
        pass
