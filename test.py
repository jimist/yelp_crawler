from Crawlers import Crawler
import json
import time
import sys

myCrawler = Crawler()
with open('Restaurant-urls.json', 'r') as f:
    restaurantDict = json.load(f)
with open('CoffeeShop-urls.json', 'r') as f:
    coffeeshopDict = json.load(f)
targetList = coffeeshopDict + restaurantDict

sys.stdout.write(str(len(targetList)))

counter = 0
for restUrl in targetList:
    counter+=1
    targetUrl = "https://www.yelp.com"+restUrl['url']
    try:
        myCrawler.getData(targetUrl)
        sys.stdout.write(str(counter)+"\n")
        sys.stdout.flush()

    except Exception as e:
        print(e)
        time.sleep(5)



