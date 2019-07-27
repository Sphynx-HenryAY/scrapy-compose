
from .abc import AbstractConnection

class MongodbConnection( AbstractConnection ):

	from scrapy.utils.project import get_project_settings
	settings = get_project_settings()

	host = settings.get( "MONGO_URI" )
	dbname = settings.get( "BOT_NAME" )

	_coll = None

	@property
	def db( self ):
		if self._db is None:
			self._db = self.client[ self.dbname ]
		return self._db

	@property
	def coll( self ):
		if self._coll is None:
			self._coll = self.db[ self.collection ]
		return self._coll

	def _init_connection( self ):
		import pymongo
		return pymongo.MongoClient( self.host )

	def shutdown( self ):
		self.client.close()

	def create( self, item ):
		return self.coll.insert_one( dict( item ) ).acknowledged

	def read( self, *args, **kwargs ):
		return self.coll.find( *args, **kwargs )
