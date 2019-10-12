import random, string

def genuid( length = 22 ):
	return ''.join( random.choice( string.ascii_letters + string.digits ) for x in range( length ) )
