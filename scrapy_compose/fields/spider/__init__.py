from scrapy_compose.load import package as load_package
from .fields import SpiderFields

load_package( __name__, vars(), lambda c: SpiderFields.register( c ) )
