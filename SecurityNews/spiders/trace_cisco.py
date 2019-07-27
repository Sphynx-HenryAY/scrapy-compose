
import json
import datetime

from SecurityNews.spiders.base import TIPSpider
from SecurityNews.items import SecurityNewsItem

class TraceCiscoSpider(TIPSpider):
	sanitize = {
		"\"RequestDispatcher\"": "'RequestDispatcher'"
	}
	name = "trace_cisco"

	allowed_domains = ['tools.cisco.com']


	def start_requests(self):
		base_url = 'https://tools.cisco.com/security/center/publicationService.x?criteria=exact&cves=&keyword=&last_published_date=&limit=100&offset={offset}&publicationTypeIDs=1,3,6,9&securityImpactRatings=&sort=-day_sir&title='

		self.not_done = True
		i = 0
		while self.not_done:
			yield scrapy.Request( base_url.format( offset = i ), callback = self.parse_content_table )
			i+=100

	def parse_content_table(self, response):

		bugs = response.css( 'body p::text' ).get()

		for k, v in self.sanitize.items():
			bugs = bugs.replace( k, v )

		bugs = json.loads( bugs )

		if not bugs:
			self.not_done = False

		timestamp = datetime.datetime.now().strftime( "%Y-%m-%d" )
		
		for bug in bugs:

			bug_id = bug[ "id" ]
			if bug_id == 1 or bug_id == 3:
				bug['Cisco_product'] = True
			elif bug_id == 6 or bug_id == 9:
				bug['Cisco_product'] = False

			bug['timestamp'] = timestamp

			yield SecurityNewsItem.DynamicItem( **bug )
