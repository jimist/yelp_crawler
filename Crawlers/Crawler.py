from DataProviders import DataProviderService
from Models import CrawlData
import requests

class Crawler():
	def __init__(self):
		self.session = DataProviderService.getSession()

	def checkDatabaseForUrl(self, url):
		result = self.session.query(CrawlData).filter(CrawlData.url == url).first()
		if result is None:
			return False
		return result

	def getData(self, url):
		data = self.checkDatabaseForUrl(url)
		if data is False:
			tempCrawlData = CrawlData()
			tempCrawlData.url = url

			response = requests.get(url)
			tempCrawlData.body = response.text

			self.session.add(tempCrawlData)
			self.session.commit()
			return tempCrawlData
		else:
			return data.body
