from abc import (
	ABC as AbstractClass,
	abstractmethod,
	abstractproperty
)

class AbstractConnection( AbstractClass ):

	host     :str = None
	port     :int = None

	username :str = None
	password :str = None

	dbname   :str = None

	_client = None
	_db = None

	def __init__( self, **kwargs ):

		for k, v in kwargs.items():
			setattr( self, k, v )

	@property
	def client( self ):
		if self._client is None:
			self._client = self._init_connection()
		return self._client

	@abstractproperty
	def db( self ): pass

	@abstractmethod
	def _init_connection( self ): pass

	@abstractmethod
	def shutdown( self ): pass

	@abstractmethod
	def create( self ): pass

	@abstractmethod
	def read( self ): pass

	def update( self ): pass

	def delete( self ): pass

	def filter( self ): pass
