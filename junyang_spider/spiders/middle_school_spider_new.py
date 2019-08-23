# -*- coding: utf-8 -*-
import scrapy
from junyang_spider.items import MiddleSchoolItem


class MiddleSchoolSpider(scrapy.Spider):
    name = "middle_school_spider_new"
    allowed_domains = ["zhongkao.com", ]
    start_urls = ["http://school.zhongkao.com/province/0/p1/", ]
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_data.pipelines.MiddleSchoolPipeline': 200},

    }

    def parse(self, response):
        for a in response.css("h3 a"):
            url = a.css("::attr('href')").extract_first()
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_school)
        for i in range(2, 5433):
            next_page_url = "http://school.zhongkao.com/province/0/p%s/" % i
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_school(self, response):

        school = response.css("nav.wrapper a::text").extract()
        if len(school) == 5:
            item = MiddleSchoolItem()
            item['province'] = school[1].split(u"学校库")[0].strip()
            item['city'] = school[2].strip()
            item['district'] = school[3].strip()
            item['school_name'] = school[4].strip()
            yield item
        elif len(school) == 4:
            item = MiddleSchoolItem()
            province = school[1].split(u"学校库")[0].strip()
            if province in (u"北京", u"天津", u"重庆", u"上海"):
                item['province'] = school[1].split(u"学校库")[0].strip()
                item['city'] = item['province']
                item['district'] = school[2].strip()
                item['school_name'] = school[3].strip()
                yield item
        # for a in response.css("a.org"):
        #     item = MiddleSchoolItem()
        #     item['province'] = response.meta['province']
        #     item['city'] = response.meta['city']
        #     item['school_name'] = a.css("::text").extract_first()
        #     yield item
