
def realize( selector, query ):
	if not query.startswith( "@" ):
		return query

	sel_list = selector( query[1:] )

	syntax = selector.__name__
	text_sufx = "::text" if syntax == "css" else "text()"

	if not query.endswith( text_sufx ):
		xel_list = sel_list.xpath( "string()" )
		# if xpath string is applicable, use it
		if xel_list:
			sel_list = xel_list

	return sel_list.get( "" ).strip()

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
