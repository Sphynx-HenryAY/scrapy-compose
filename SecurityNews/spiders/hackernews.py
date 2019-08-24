# -*- coding: utf-8 -*-
import scrapy


class HackernewsSpider(scrapy.Spider):
    name = 'hackernews'
    allowed_domains = ['thehackernews.com']
    start_urls = ['http://thehackernews.com/']

    def parse(self, response):
        pass
