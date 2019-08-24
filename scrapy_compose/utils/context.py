
def realize( selector, query ):
	if not query.startswith( "@" ):
		return query

	sel_list = selector( query[1:] )

	xel_list = sel_list.xpath( "string()" )
	if xel_list:
		sel_list = xel_list

	if len( sel_list ) < 2:
		return sel_list.get( "" ).strip()

	return sel_list.extract()

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
