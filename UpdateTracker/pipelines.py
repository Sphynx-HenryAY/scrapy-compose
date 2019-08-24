
class LastUpdatePipeline:

	name = "LastUpdate"

	timestamp_format = "%Y-%m-%d"
	_timestamp = None

	fringerprints = {}

	@classmethod
	def from_crawler( cls, crawler ):
		p = cls()
		p.fingerprints = {}
		return p

	@property
	def timestamp( self ):
		if not self._timestamp:
			from datetime import datetime
			self._timestamp = ( datetime
				.utcnow()
				.strftime( self.timestamp_format )
			)
		return self._timestamp


	def open_spider( self, spider ):
		from common.db.mongo import MongodbConnection
		self.mongo = MongodbConnection(
			dbname = self.name,
			collection = spider.name,
		)

	def process_item( self, item, spider ):
		if "id" in item and item[ "id" ]:
			item_id = item[ "id" ]
			self.mongo.coll.update( 
				{ "id": item_id },
				{
					"id": item_id,
					"last_update": self.timestamp,
					"fringerprint": self.get_fingerprint( spider )
				},
				upsert = True,
			)
		else:
			spider.logger.warn( f"{self.name} can not process this item from {spider.name}" )

		return item

	def get_fingerprint( self, spider ):
		s_name = spider.name
		fps = self.fringerprints
		if s_name in fps:
			return fps[ s_name ]

		from os.path import getmtime
		from scrapy_compose.load import resource as load_resource

		s_file = load_resource( spider.__module__ ).__file__

		fp = {
			"spider": s_name,
			"spider_modified": getmtime( s_file ),
		}

		if hasattr( spider.__class__, "spider-config" ):
			fp[ "compose_modified" ] = getmtime( f"{s_file.rsplit('.', 1)[0]}.yml" )

		import json
		return json.dumps( fp )
