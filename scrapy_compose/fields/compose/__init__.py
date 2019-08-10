from scrapy_compose.load import package as load_package
from .fields import ComposeFields

load_package( __name__, vars(), lambda c: ComposeFields.register( c ) )
