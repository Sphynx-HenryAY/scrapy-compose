
from scrapy import Item, Field

__all__ = [ "DynamicItem" ]

class EmptyItem( Item ):

	@classmethod
	def DynamicItem( cls, **kwargs ):
		cls.fields = { k: Field() for k in kwargs }
		return cls( **kwargs )

DynamicItem = EmptyItem.DynamicItem
