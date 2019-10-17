"""
@version:1.0
@author: endaqa
@file paper_ewt360.py
@time 2019/10/15 10:46
"""
# -*- coding: utf-8 -*-
import scrapy
from junyang_spider.items import PaperEWTItem


class PaperEWT360(scrapy.Spider):
    name = "paper_ewt360"
    allowed_domains = ["ewt360.com"]
    # start_urls = [
    #     "https://www.ewt360.com/Review/Lists?page=1",
    # ]
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.PaperEWTPipeline': 200}
    }

    headers = {
        'Cookie': "big_data_cookie_id=5932bf48-8421-dcd4-fca2-11c5f7247922%7C1571283046904; Hm_lvt_=1571283047; Hm_mstid_=62075284295976; _ga=GA1.2.1517150177.1571283047; _gid=GA1.2.2042020364.1571283047; Hm_lvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571283048; Hm_lvt_5261308991055a39373a5ccf8edd3695=1571283048; UserID=15045901; user=tk=15045901-1-2205186270f9c379&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uT6MmsUKCjgTyrQvtEdgy60irHXjacgdaD3imiX9jABy9%0A61w6GB6nOIej2MWapRiDEFjegLZ6RSZcUB4ROC+eqX/xZlKtcpnkSDpR5UHSAN+dkwMKgV8mOg==; ewt_user=tk=15045901-1-2205186270f9c379&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uT6MmsUKCjgTyrQvtEdgy60irHXjacgdaD3imiX9jABy9%0A61w6GB6nOIej2MWapRiDEFjegLZ6RSZcUB4ROC+eqX/xZlKtcpnkSDpR5UHSAN+dkwMKgV8mOg==; token=15045901-1-2205186270f9c379; Hm_lpvt_=1571290984; Hm_lpvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571290984; Hm_lpvt_5261308991055a39373a5ccf8edd3695=1571290984",
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "8c2edf16-39c6-48d8-94c5-c7142412291f,1a9b8e21-c718-4aa1-a454-b237d6687ee5",
        'Host': "www.ewt360.com",
        'Accept-Encoding': "gzip, deflate",
        'cache-control': "no-cache"
    }

    def start_requests(self):

        for i in range(2, 3):
            url = "https://www.ewt360.com/Review/Lists?page=%s" % i
            yield scrapy.Request(url, method="GET", headers=self.headers, callback=self.parse)

    def parse(self, response):
        # item = PaperEWTItem()
        # print(response.css("tr:nth-of-type(2) td::text").extract()[1].strip())
        # item['data_category'] = response.css(
        #     "div.videoFZ > table > tbody > tr:nth-child(1) > td::text").extract_first()
        # print(item)
        for paper in response.css('li.pngFix'):
            href = paper.css("a::attr('href')")

            paper_url = href.extract_first()
            url = response.urljoin(paper_url)
            print(url)
            # requests_header = {
            #     'User-Agent': 'PostmanRuntime/7.17.1',
            #     'Accept': '*/*',
            #     'Cache-Control': 'no-cache',
            #     'Postman-Token': '1e3e699a-b9e2-4c89-9980-0619b2aa3364',
            #     'Host': 'www.ewt360.com',
            #     'Accept-Encoding': 'gzip, deflate',
            #     'Connection': 'keep-alive'
            # }
            yield scrapy.Request(url, method="GET", callback=self.parse_contents, headers=self.headers)

        #     if paper_url.find("http") != -1:
        #         item = YouzySchoolBadgeItem()
        #         item['school_name'] = school.css('a.name::text').extract_first()
        #         item['image_url'] = image_url
        #         yield item
        # for i in range(2, 144):
        #     yield scrapy.Request('https://www.youzy.cn/college/search?page=%d' % i, callback=self.parse)

    def parse_contents(self, response):
        pass
        # print(response.headers)
        # print(response.css("tr:nth-of-type(2) td::text").extract()[1].strip())
        # item = PaperEWTItem()
        # item['data_category'] = response.css("div.videoFZ > table > tbody > tr:nth-child(1) > td::text").extract_first()
        # print(item)
