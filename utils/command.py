
def spider_filter( s_list, pattern ):
	import re
	regex = re.compile( pattern )
	return [ s for s in s_list if regex.search( s ) ]
