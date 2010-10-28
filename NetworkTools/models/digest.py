class Digest:
	def __init__(self, title, participants, unread, total, date):
		self.title = title
		self.participants = participants
		self.unread_count = unread
		self.blip_count = total
		self.date = date
		self.extras = []
		self.folder = None

	@property
	def addresses(self):
		return [i.addr for i in self.participants]

class SearchResults:
	def __init__(self, query, page, digests=[], maxpage = None):
		self.query=query
		self.page=page
		if maxpage == None:
			self.maxpage = self.page+1
		else:
			self.maxpage = maxpage
		self.digests = digests

	@property
	def num_results(self):
		return len(self.digests)
