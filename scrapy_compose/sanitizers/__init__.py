
from .strip import default as strip
from .split import default as split
from .join import default as join

def concreted( str_arr ):
	concrete = []
	for x in str_arr:
		x_strip = x.strip()
		if x_strip:
			concrete.append( x_strip )
	return concrete
