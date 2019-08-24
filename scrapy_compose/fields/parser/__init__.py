from scrapy_compose.load import package as load_package
from .fields import ParserFields

load_package( __name__, vars(), lambda c: ParserFields.register( c ) )
