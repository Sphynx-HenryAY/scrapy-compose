
class Utils:

	@staticmethod
	def realize( selector, query ):
		if query.startswith( "@" ):
			selected = selector( query[1:] )
			if not selected:
				return ""
			if len( selected ) == 1:
				return selected.get().strip()
			return "".join( selected.extract() ).strip()
		return query

	@staticmethod
	def xtring( selector ):
		len_selected = len( selector )
		if len_block < 2:
			return [ selector.xpath( "string()" ).get( "" ).strip() ]
		return [ x.strip() for x in selector.xpath( "string()" ).extract() ]

	@staticmethod
	def stripped( str_arr ):
		concrete = []
		for x in str_arr:
			x_strip = x.strip()
			if x_strip:
				concrete.append( x_strip )
		return concrete

	@staticmethod
	def tablize(
			table = None,
			thead = None, qhead = None,
			qrows = None, qrow = None,
			row_process = lambda x: x.extract()
		):

		syntax = table.__name__
		headers = thead or table( qhead ).extract()

		return list(
			dict( zip(
				headers,
				row_process( getattr( row, syntax )( qrow ) )
			) )
			for row in table( qrows )
		)
