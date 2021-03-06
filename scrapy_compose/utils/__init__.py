
from sys import version_info
import random, string

def genuid( length = 22 ):
	choices = string.ascii_letters + string.digits
	return ''.join( random.choice( choices ) for x in range( length ) )

if version_info.major == 2:
	class classproperty( property ):
		def __get__(self, obj, klass=None):
			if klass is None:
				klass = type( obj )
			if self.fget is None:
				raise AttributeError("unreadable attribute")
			return self.fget( klass )
else:
	class classproperty:
		def __init__( self, f ):
			self.f = classmethod( f )

		def __get__( self, *args ):
			return self.f.__get__( *args )()
