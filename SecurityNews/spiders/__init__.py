# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

# Commented scrapy.utils.spider:27 to load all spiders declared and with name

from SecurityNews.utils.load import co_spiders as load_co_spiders
vars().update( load_co_spiders( "UpdateTracker.spiders" ) )
vars().update( load_co_spiders( "BugInfo.spiders" ) )
