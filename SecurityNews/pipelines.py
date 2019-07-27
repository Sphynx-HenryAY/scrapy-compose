# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class SecuritynewsPipeline(object):

	def process_item(self, item, spider):
		return item

class MongoPipeline(object):

	@classmethod
	def from_crawler(cls, crawler):
		return cls()

	def open_spider(self, spider):
		from SecurityNews.db.mongo import MongodbConnection
		self.mongo = MongodbConnection(
			collection = spider.name
		)

	def close_spider( self, spider ):
		self.mongo.shutdown()

	def process_item(self, item, spider):
		self.mongo.create( item )
		return item
