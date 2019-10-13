import random, string

def genuid( length = 22 ):
	return ''.join( random.choice( string.ascii_letters + string.digits ) for x in range( length ) )

class classproperty:
	def __init__( self, f ):
		self.f = classmethod( f )

	def __get__( self, *args ):
		return self.f.__get__( *args )()
