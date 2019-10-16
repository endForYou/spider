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
    cookies = {
        'Cookie': 'big_data_cookie_id=c127ee56-2676-493a-6684-f90d051e9258%7C1571208883630; Hm_lvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571208719; Hm_lvt_5261308991055a39373a5ccf8edd3695=1571208719; _ga=GA1.2.1210832376.1571208885; _gid=GA1.2.1144140080.1571208885; UserID=15045901; user=tk=15045901-1-10ccccd332dc5e98&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uT6MmsUKCjgSxY3PAl/r0WjzKOPmgmbE6AoPV2iFiO53u%0Ax/fI6yCiAjhPOsB9UmgdYvrGV7VCkUZTi6N6e8D0RjxvtNaAIhdRKqOhqnXgg3G7lVtITZXJkg==; ewt_user=tk=15045901-1-10ccccd332dc5e98&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uT6MmsUKCjgSxY3PAl/r0WjzKOPmgmbE6AoPV2iFiO53u%0Ax/fI6yCiAjhPOsB9UmgdYvrGV7VCkUZTi6N6e8D0RjxvtNaAIhdRKqOhqnXgg3G7lVtITZXJkg==; token=15045901-1-10ccccd332dc5e98; Hm_lvt_=1571208719,1571208885,1571216284; Hm_lpvt_=1571216297; Hm_lpvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571216297; Hm_lpvt_5261308991055a39373a5ccf8edd3695=1571216297 '}

    def start_requests(self):
        requests_header = {
            'Host': 'www.ewt360.com',
            'Sec-Fetch-User': '?1',
            'Cookie': 'big_data_cookie_id=0adcfa69-faef-cf96-9a00-3c1d3a2951ab%7C1571221516820; Hm_mstid_=364082011237368; Hm_lvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571221517; Hm_lvt_5261308991055a39373a5ccf8edd3695=1571221517; _ga=GA1.2.335479032.1571221517; _gid=GA1.2.1367627752.1571221517; UserID=15045901; user=tk=15045901-1-ade7b2cc3bb01ae8&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uT6MmsUKCjgS8flZfN58nLjzXhJJHWJ5paaGEwobNo9Xu%0A2UMfJnwAo8nitAZdiaGMCIZYkpHID6QVkBx0k32A2kouSJtWPTOmumMyoNzVDxvqSxxPK4q5cQ==; ewt_user=tk=15045901-1-ade7b2cc3bb01ae8&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uT6MmsUKCjgS8flZfN58nLjzXhJJHWJ5paaGEwobNo9Xu%0A2UMfJnwAo8nitAZdiaGMCIZYkpHID6QVkBx0k32A2kouSJtWPTOmumMyoNzVDxvqSxxPK4q5cQ==; token=15045901-1-ade7b2cc3bb01ae8; Hm_lvt_=1571221517,1571221647; _gat=1; Hm_lpvt_=1571221649; Hm_lpvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571221649; Hm_lpvt_5261308991055a39373a5ccf8edd3695=1571221649'
        }

        for i in range(1, 2):
            url = "https://www.ewt360.com/Review/Lists?page=%s" % i
            yield scrapy.Request(url, method="GET", headers=requests_header, callback=self.parse)

    def parse(self, response):
        # item = PaperEWTItem()
        # print(response.css("tr:nth-of-type(2) td::text").extract()[1].strip())
        # item['data_category'] = response.css(
        #     "div.videoFZ > table > tbody > tr:nth-child(1) > td::text").extract_first()
        # print(item)
        requests_header = {
            'Host': 'www.ewt360.com',
            'Sec-Fetch-User': '?1',
            'Cookie': 'big_data_cookie_id=0adcfa69-faef-cf96-9a00-3c1d3a2951ab%7C1571221516820; Hm_mstid_=364082011237368; Hm_lvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571221517; Hm_lvt_5261308991055a39373a5ccf8edd3695=1571221517; _ga=GA1.2.335479032.1571221517; _gid=GA1.2.1367627752.1571221517; UserID=15045901; user=tk=15045901-1-ade7b2cc3bb01ae8&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uT6MmsUKCjgS8flZfN58nLjzXhJJHWJ5paaGEwobNo9Xu%0A2UMfJnwAo8nitAZdiaGMCIZYkpHID6QVkBx0k32A2kouSJtWPTOmumMyoNzVDxvqSxxPK4q5cQ==; ewt_user=tk=15045901-1-ade7b2cc3bb01ae8&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uT6MmsUKCjgS8flZfN58nLjzXhJJHWJ5paaGEwobNo9Xu%0A2UMfJnwAo8nitAZdiaGMCIZYkpHID6QVkBx0k32A2kouSJtWPTOmumMyoNzVDxvqSxxPK4q5cQ==; token=15045901-1-ade7b2cc3bb01ae8; Hm_lvt_=1571221517,1571221647; _gat=1; Hm_lpvt_=1571221649; Hm_lpvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571221649; Hm_lpvt_5261308991055a39373a5ccf8edd3695=1571221649'
        }
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
            yield scrapy.Request(url, method="GET",callback=self.parse_contents, headers=requests_header)

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
