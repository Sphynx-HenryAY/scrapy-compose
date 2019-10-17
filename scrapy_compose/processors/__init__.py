
def concreted( str_arr ):
	concrete = []
	for x in str_arr:
		x_strip = x.strip()
		if x_strip:
			concrete.append( x_strip )
	return concrete

class Split:
	def __init__( self, sep = None, maxsplit = -1 ):
		self.sep = sep
		self.maxsplit = maxsplit

	def __call__( self, s ):
		return s.split( sep = self.sep, maxsplit = self.maxsplit )

class Strip:
	def __init__( self, chars = None ):
		self.chars = chars

	def __call__( self, s ):
		return s.strip( self.chars )
