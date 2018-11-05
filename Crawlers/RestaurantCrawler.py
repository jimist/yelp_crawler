import Crawlers.Crawler as Crawler
from lxml import html
from lxml import etree

class RestaurantCrawler(Crawler):
	def __init__(self, city):
		super(RestaurantCrawler, self).__init__()
		self.city = city

	def getListByCity(self):
		print(self.city)
		url = "https://www.yelp.com/search?find_desc={}&find_loc={}&ns=1".format("Restaurants", self.city)
		htmlData = self.getData(url)
		tree = html.fromstring(htmlData)

	def getSingleDetails():
		print("get single details")

	def getGalleryPhotoList(name):
		print("get  gallery photo list")

	def getCommentsByPhoto(name):
		print("get list of all comments with their Photo")