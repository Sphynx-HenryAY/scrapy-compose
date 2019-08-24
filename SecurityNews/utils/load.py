
def co_spiders( module, namespace = None, naming = None ):

	if namespace is None: namespace = {}

	from inspect import isclass
	from scrapy import Spider
	from scrapy_compose.load import package as load_package

	spiders = load_package( module, key = lambda s: (
		isclass( s ) and
		issubclass( s, Spider ) and
		getattr( s, "name", None )
	) )

	for s_name, spider in spiders.items():

		if naming:
			spider.name = naming.format( **locals() )
		else:
			spider.name = f"{spider.name}.{module.split('.',1)[0]}"

		namespace[ s_name ] = spider

	return namespace
