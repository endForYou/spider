# -*- coding: utf-8 -*-
import scrapy
from junyang_spider.items import BaiduSchoolItem

urls = []
for i in range(1, 33):
    urls.append("http://kaoshi.edu.sina.com.cn/college/scorelist?tab=&wl=&local=%d&provid=&batch=&syear=&page=1" % i)


class SinaSpider(scrapy.Spider):
    name = "sina_spider"
    allowed_domains = ["sina.com.cn", ]
    start_urls = urls
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_data.pipelines.SchoolEntryScorePipeline': 200},

    }

    def parse(self, response):
        for tr in response.css("tr.tbl2tbody:nth-of-type(n+2)"):
            item = BaiduSchoolItem()
            item['school'] = tr.css(" td:nth-of-type(1) > a::text").extract_first()
            item['province'] = tr.css(" td:nth-of-type(2)::text").extract_first()
            item['curriculum'] = tr.css(" td:nth-of-type(3)::text").extract_first()
            item['batch'] = tr.css(" td:nth-of-type(4)::text").extract_first()
            item['year'] = tr.css(" td:nth-of-type(5)::text").extract_first()
            item['max'] = tr.css(" td:nth-of-type(6)::text").extract_first()
            item['average'] = tr.css(" td:nth-of-type(7)::text").extract_first()
            if item:
                yield item
        pages = int(response.css("div.pageNumWrap::attr('totalpage')").extract_first())
        # print(response.url)
        for page in range(2, pages+1):
            url = response.url.split("page=")[0]
            next_url = url + "page=%d" % page
            # next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
