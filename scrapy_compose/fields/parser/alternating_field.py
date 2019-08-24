
from .field import ParserField as BaseField

class AlternatingField( BaseField ):

	sanitize_timing = [ "pre_pack", "packing", "post_pack" ]

	@property
	def context( self ):
		if not self._context:

			value = self.value
			rk, rv = value.get( "key", "" ), value.get( "value", "" )
			if (
				( rk and rk.startswith( "@" ) ) and
				( rv and rv.startswith( "@" ) )
			):
				krows, vrows = self.query_context()
			else:
				krows, vrows = self.text_context()

			self._context = self.post_pack( dict( zip( krows, vrows ) ) )

		return self._context

	def is_text_query( self, query ):
		return query.endswith( "::text" if self.syntax == "css" else "text()" )

	def query_context( self ):

		rows = self.selector( self.key[1:] )
		rows_sel = getattr( rows, self.syntax )

		value = self.value
		rk, rv = value[ "key" ][1:], value[ "value" ][1:]

		selected = []
		packing = self.packing
		is_text_query = self.is_text_query

		for query in [ rk, rv ]:
			sub_rows = rows_sel( query )

			if not is_text_query( query ):
				sub_rows = sub_rows.xpath( "string()" )

			prepacked = self.pre_pack( sub_rows.extract() )

			selected.append( [
				self.packing( x ) for x in prepacked
			] )

		return selected

	def text_context( self ):

		key = self.key[1:]

		rows = self.selector( key )
		if not self.is_text_query( key ):
			rows = rows.xpath( "string()" )

		prepacked = self.pre_pack( rows.extract() )
		packing = self.packing
		rows = [ packing( x ) for x in prepacked ]

		return rows[0::2], rows[1::2]
