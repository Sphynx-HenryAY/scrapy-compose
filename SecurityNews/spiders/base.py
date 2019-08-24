
import scrapy

class TIPSpider( scrapy.Spider ):

	_flag = """
				   _____                                 _    __              
				  / ___/  ___   _____  __  __   _____   (_)  / /_   __  __    
				  \__ \  / _ \ / ___/ / / / /  / ___/  / /  / __/  / / / /    
				 ___/ / /  __// /__  / /_/ /  / /     / /  / /_   / /_/ /     
				/____/  \___/ \___/  \__,_/  /_/     /_/   \__/   \__, /      
				                                                 /____/       
				                                _   __                        
				                               / | / /  ___  _      __   _____
				                              /  |/ /  / _ \| | /| / /  / ___/
				                             / /|  /  /  __/| |/ |/ /  (__  ) 
				                            /_/ |_/   \___/ |__/|__/  /____/  
	"""

	def showflag( self ):
		self.log( self._flag )

	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )

		import json
		self.log = lambda *args, **kwargs: self.logger.info(
			"|" +
			", ".join( str( e ) for e in args ) +
			"|" +
			( json.dumps( kwargs, indent = 4 ) if kwargs else "" )
		)

	def parse( self, response ):
		pass
