import json

import scrapy
from lxml import html
from scrapy.crawler import CrawlerProcess
from scrapy import Selector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI as engine, MUST_DOWNLOAD_USER_IMAGE, BASE_DIR
from Models import Business, CrawlData, Working_Hours, Review, YelpUser
import requests
import os


class RestaurantSpider(scrapy.Spider):
    name = "restaurants"
    start_urls = [
        "https://www.yelp.com/search?cflt=restaurants&find_loc=London&start=0"
    ]

    def parse(self, response):
        for biz in response.xpath(
            "//div[@class='lemon--div__373c0__6Tkil largerScrollablePhotos__373c0__3FEIJ arrange__373c0__UHqhV border-color--default__373c0__2oFDT']"
        ):
            yield {"url": biz.css('a::attr("href")').extract_first()}

        next_page = response.css(
            'link[rel="next"]::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        # else:
        #     yield{
        #         'all-done':'True'
        #     }


class CoffeeShopSpider(scrapy.Spider):
    name = "CoffeeShops"
    start_urls = [
        "https://www.yelp.com/search?cflt=coffee&find_loc=London&start=0"]

    def parse(self, response):
        for biz in response.xpath(
            "//div[@class='lemon--div__373c0__6Tkil largerScrollablePhotos__373c0__3FEIJ arrange__373c0__UHqhV border-color--default__373c0__2oFDT']"
        ):
            yield {"url": biz.css('a::attr("href")').extract_first()}

        next_page = response.css(
            'link[rel="next"]::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


class BusinessFetch(scrapy.Spider):
    def __init__(self, jsonfile):
        self.db_engine = create_engine(engine, echo=True)
        self.db_session = sessionmaker(bind=self.db_engine,autoflush=True)
        self.session = self.db_session()
        with open(jsonfile, "r") as resfile:
            self.res_links = json.load(resfile)
        self.start_urls = ["https://www.yelp.com" + self.res_links[0]["url"]]

    def fill_workinghours(self, response, day_number):
        table = Selector(response)
        day = table.xpath('//table[@class="table table-simple hours-table"]/tbody/tr')[
            day_number
        ]
        working_hours = day.xpath(".//span/text()").extract()
        times = ""
        if(len(working_hours) > 0):
            for td in working_hours:
                times += td.strip() + " "
        else:
            times = "Closed"
        return times.strip()

    def parse(self, response):
        if (self.session.query(CrawlData).filter(CrawlData.url == response.url).count() == 0):
            biz = Business()
            biz.id = response.xpath(
                '//div[@class="lightbox-map hidden"]/@data-business-id'
            ).extract_first()
            biz.address = response.xpath(
                '//div[@class="lightbox-map hidden"]/@data-business-address'
            ).extract_first()
            location = json.loads(
                response.xpath(
                    '//div[@class="lightbox-map hidden"]/@data-map-state'
                ).extract_first()
            )
            biz.city = (
                response.xpath('//small[@class="biz-city"]/text()')
                .extract_first()
                .strip()
            )
            biz.latitude = location["center"]["latitude"]
            biz.longitude = location["center"]["longitude"]
            biz.name = (
                response.xpath(
                    '//h1[@class="biz-page-title embossed-text-white shortenough"]/text()'
                )
                .extract_first()
                .strip()
            )
            biz.review_count = (
                response.xpath(
                    '//span[@class="review-count rating-qualifier"]/text()'
                )
                .extract_first()
                .strip()
            )
            biz.review_count = biz.review_count[: biz.review_count.find(
                " ")]
            biz.stars = response.xpath(
                '//div[contains(@class,"i-stars")]/@title'
            ).extract_first()
            biz.stars = biz.stars[: biz.stars.find(" ")]
            self.session.add(biz)

            working_hours = Working_Hours()
            working_hours.biz_id = biz.id
            working_hours.monday = self.fill_workinghours(response, 0)
            working_hours.tuesday = self.fill_workinghours(response, 1)
            working_hours.wednesday = self.fill_workinghours(response, 2)
            working_hours.thursday = self.fill_workinghours(response, 3)
            working_hours.friday = self.fill_workinghours(response, 4)
            working_hours.saturday = self.fill_workinghours(response, 5)
            working_hours.sunday = self.fill_workinghours(response, 6)
            self.session.add(working_hours)

            cp = CrawlerProcess(
                {"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}
            )
            cp.crawl(ReviewFetch, start_url=response.url, biz_id=biz.id)
            cp.start(stop_after_crawl=False)

            if (self.session.query(CrawlData).filter(CrawlData.url == response.url).count() != 0):
                crawl_data = CrawlData()
                crawl_data.body = response.body
                crawl_data.requestHeader = str(response.request.headers)
                crawl_data.url = response.url
                self.session.add(crawl_data)

            self.session.commit()

        del self.res_links[0]
        if len(self.res_links) != 0:
            yield response.follow(
                "https://www.yelp.com" + self.res_links[0]["url"], self.parse
            )


class ReviewFetch(scrapy.Spider):
    compliments = {
        'icon icon--18-compliment icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'Thank You',
        'icon icon--18-pencil icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'Good Writer',
        'icon icon--18-file icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'Just a Note',
        'icon icon--18-write-more icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'Write More',
        'icon icon--18-camera icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'Great Photo',
        'icon icon--18-funny icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'You are Funny',
        'icon icon--18-heart icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'Cute Pic',
        'icon icon--18-flame icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'Hot Stuff',
        'icon icon--18-profile icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'Like Your Profile',
        'icon icon--18-cool icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'You are Cool',
        'icon icon--18-list icon--size-18 icon--white icon--fallback-inverted u-sticky-top': 'Great Lists'
    }

    def __init__(self, start_url, biz_id):
        self.start_urls = [start_url]
        self.biz_id = biz_id
        self.db_engine = create_engine(engine, echo=True)
        self.db_session = sessionmaker(bind=self.db_engine,autoflush=True)
        self.session = self.db_session()

    def fetch_userdata(self, url):
        user = YelpUser()
        response = requests.get(url)
        page = Selector(response)
        user.yelp_id = url[url.rfind('=')+1:]
        user.name = page.xpath(
            '//div[@class="user-profile_info arrange_unit"]/h1/text()').extract_first()
        user.location = page.xpath(
            '//div[@class="user-profile_info arrange_unit"]/h3/text()').extract_first()
        user.tagline = page.xpath(
            '//p[@class="user-tagline"]/text()').extract_first()
        user.friends_count = page.xpath(
            '//li[@class="friend-count"]/strong/text()').extract_first()
        user.reviews_count = page.xpath(
            '//li[@class="review-count"]/strong/text()').extract_first()
        user.photos_count = page.xpath(
            '//li[@class="photo-count"]/strong/text()').extract_first()
        user.image_url = page.xpath(
            '//div[@class="user-profile_avatar"]//img/@src').extract_first()

        if(MUST_DOWNLOAD_USER_IMAGE):
            if(os.path.exists(BASE_DIR+'/UserImages') == False):
                os.mkdir(BASE_DIR+'/UserImages')
            with open(BASE_DIR+'UserImages/'+user.yelp_id+'.jpg', 'wb') as f:
                f.write(requests.get(user.image_url))
            user.image_path = BASE_DIR+'UserImages/'+user.yelp_id+'.jpg'

        sidebar = page.xpath('//div[@class="user-details-overview_sidebar"]')
        extra_data = {}
        for ysection in sidebar.xpath('.//div[@class="ysection"]'):
            key = ysection.xpath('.//h4/text()').extract_first()
            if(key == 'Rating Distribution'):
                starts_distribution = ysection.xpath(
                    './/td[@class="histogram_count"]/text()').extract()
                extra_data[key] = dict()
                extra_data[key]['5 stars'] = starts_distribution[0]
                extra_data[key]['4 stars'] = starts_distribution[1]
                extra_data[key]['3 stars'] = starts_distribution[2]
                extra_data[key]['2 stars'] = starts_distribution[3]
                extra_data[key]['1 stars'] = starts_distribution[4]
            elif(key == 'Review Votes' or key == 'Stats'):
                items = ysection.xpath('.//ul/li')
                items_title = ysection.xpath(
                    './/ul/li/text()[not(normalize-space(.)="")]').extract()
                for item in items_title:
                    item = item.strip()
                extra_data[key] = dict()
                for title, item in dict(zip(items_title, items)).items():
                    extra_data[key][title.strip()] = item.xpath(
                        './/strong/text()').extract_first()
            elif(key.find('Compliments') != -1):
                items = ysection.xpath('.//li')
                extra_data['Compliments'] = dict()
                for item in items:
                    compliment = item.xpath('.//span/@class').extract_first()
                    extra_data['Compliments'][self.compliments[compliment]] = item.xpath(
                        './/small/text()').extract_first()
        user.meta = json.dumps(extra_data)
        return user

    def parse(self, response):
        page = Selector(response)
        review_boxes = page.xpath(
            '//ul[@class="ylist ylist-bordered reviews"]/li')
        del review_boxes[0]
        for review_box in review_boxes:
            rv = Review()
            rv.business_id = self.biz_id
            rv.user_id = review_box.xpath(
                './/li[@class="user-name"]/a/@href'
            ).extract_first()
            if rv.user_id != None:
                user_url = rv.user_id
                rv.user_id = rv.user_id[rv.user_id.rfind("=") + 1:]
                if (self.session.query(YelpUser).filter(YelpUser.yelp_id == rv.user_id).count() == 0):
                    user = self.fetch_userdata('https://www.yelp.com'+user_url)
                    self.session.add(user)

            else:
                user = YelpUser()
                user.yelp_id = None
                user.name = "Qype User"
                user.location = review_box.xpath(
                    './/li[@class="user-location responsive-hidden-small"]/b/text()'
                ).extract_first().strip()
                user.photos_count = review_box.xpath(
                    './/li[@class="photo-count responsive-small-display-inline-block"]/b/text()').extract_first()
                user.friends_count = review_box.xpath(
                    './/li[@class="friend-count responsive-small-display-inline-block"]/b/text()').extract_first()
                user.reviews_count = review_box.xpath(
                    './/li[@class="review-count responsive-small-display-inline-block"]/b/text()').extract_first()
                user.meta = None
                self.session.add(user)
            
            rv.text = review_box.xpath(
                './/div[@class="review-content"]/p/text()'
            ).extract_first()
            rv.rating = review_box.xpath(
                './/div[@class="review-content"]/div[@class="biz-rating biz-rating-large clearfix"]/div/div/@title'
            ).extract_first()
            rv.rating = rv.rating[0: rv.rating.find(" ")]
            rv.date = review_box.xpath(
                './/div[@class="review-content"]/span[@class="rating-qualifier"]/text()'
            ).extract_first()
            self.session.add(rv)

        if (self.session.query(CrawlData).filter(CrawlData.url == response.url).count() != 0):
            crawl_data = CrawlData()
            crawl_data.body = response.body
            crawl_data.requestHeader = str(response.request.headers)
            crawl_data.url = response.url
            self.session.add(crawl_data)

        self.session.commit()
        next_page = page.xpath('//link[@rel="next"]/@href').extract_first()
        if(next_page != None):
            yield response.follow(next_page, self.parse)
