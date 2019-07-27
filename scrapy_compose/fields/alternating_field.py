
from ..utils import Utils
from .field import Field

class AlternatingField( Field ):

	@property
	def content( self ):

		if self._content is None:

			value = self.value
			if (
					value.get( "key", "" ).startswith( "@" ) and
					value.get( "value", "" ).startswith( "@" )
				):
				self._content = self._content_query()
			else:
				self._content = self._content_plain()

		return self._content

	def get_data( self, selected, get_text = False ):
		if not selected:
			return ""
		if not get_text:
			selected = selected.xpath( "string()" )
		return selected.get().strip()

	def _content_plain( self ):

		syntax = self.syntax
		text_sufx = "::text" if syntax == "css" else "text()"

		key = self.key[1:]
		get_text = key.endswith( text_sufx )
		get_data = self.get_data

		rows = Utils.stripped( [ get_data( r, get_text ) for r in self.selector( key ) ] )

		return dict( zip( rows[0::2], rows[1::2] ) )

	def _content_query( self ):

		syntax = self.syntax
		text_sufx = "::text" if syntax == "css" else "text()"

		kq, vq = self.value[ "key" ][1:], self.value[ "value" ][1:]
		kget, vget = kq.endswith( text_sufx ), vq.endswith( text_sufx )

		get_data = self.get_data

		rows = self.selector( self.key[1:] )
		context = {}
		for ksel, vsel in zip( rows[0::2], rows[1::2] ):
			kdata = get_data( getattr( ksel, syntax )( kq ), kget )
			if kdata:
				context[ kdata ] = get_data( getattr( vsel, syntax )( vq ), vget )

		return context
