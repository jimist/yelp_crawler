import scrapy
from Spiders import CoffeeShopSpider,BusinessFetch,RestaurantSpider
from scrapy.crawler import CrawlerProcess
import json

process = CrawlerProcess(
    {
        "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "FEED_FORMAT": "json",
        "FEED_URI": "CoffeeShop_urls.json",
    }
)
try:
    with open("CoffeeShop_urls.json", "r") as resfile:
        pass
    process.settings['FEED_URI']=None
    process.crawl(BusinessFetch,jsonfile='CoffeeShop_urls.json')
    process.start(stop_after_crawl=False)
except FileNotFoundError:
    process.crawl(CoffeeShopSpider)
    process.start(stop_after_crawl=False)
try:
    with open("Restaurant_urls.json", "r") as resfile:
        pass
    process.settings['FEED_URI']=None
    process.crawl(BusinessFetch,jsonfile='Restaurant_urls.json')
    process.start(stop_after_crawl=False)
except FileNotFoundError:
    process.settings['FEED_URI']='Restaurant_urls.json'
    process.crawl(RestaurantSpider)
    process.start(stop_after_crawl=False)
