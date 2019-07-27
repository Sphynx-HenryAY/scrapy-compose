# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecurityNewsItem( scrapy.Item ):

	@classmethod
	def DynamicItem( cls, **kwargs ):
		cls.fields = { k: scrapy.Field() for k in kwargs }
		return cls( **kwargs )
