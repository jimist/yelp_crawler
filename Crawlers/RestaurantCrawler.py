import Crawler

class RestaurantCrawler(Crawler):
	def __init__(self, city):
		super(RestaurantCrawler, self).__init__()
		self.city = city

	def getListByCity():
		print("get List By City")

	def getSingleDetails(name):
		print("get single details")

	def getGalleryPhotoList(name):
		print("get  gallery photo list")

	def getCommentsByPhoto(name):
		print("get list of all comments with their Photo")