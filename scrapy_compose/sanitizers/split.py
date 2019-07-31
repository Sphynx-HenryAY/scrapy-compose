
from functools import partial

def default( s, by = None ):
	return s.split( by )

by_space = partial( default, by = " " )
by_linebreak = partial( default, by = "\n" )
