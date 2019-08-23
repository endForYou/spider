# -*- coding: utf-8 -*-
import scrapy
import re
import w3lib.html
from junyang_spider.items import MiddleSchoolItem


class Middle_School_Spider(scrapy.Spider):
    name = "middle_school"
    allowed_domains = ["ruyile.com"]
    start_urls = [
        "http://www.ruyile.com/xuexiao/?t=3&p=1",

    ]

    def parse(self, response):
        # print(response.css("a.hei14b"))
        for href in response.css("h4 a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        for i in range(2, 4379):
            next_url = "http://www.ruyile.com/xuexiao/?t=3&p=%d" % i
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_dir_contents(self, response):
        item = MiddleSchoolItem()
        item['school_name'] = response.css('h1::text').extract_first()
        item['location'] = response.css('div.z a::text').extract()
        item['school_nature'] = response.css('div.z:nth-of-type(2)::text').extract_first().replace("：",
                                                                                                   "") if response.css(
            'div.z:nth-of-type(2)::text').extract_first() else ""
        item['school_level'] = response.css('div.z:nth-of-type(3)::text').extract_first().replace("：",
                                                                                                  "") if response.css(
            'div.z:nth-of-type(3)::text').extract_first() else ""
        item['phone'] = response.css('div.q:nth-of-type(5)::text').extract_first().replace("：", "") if response.css(
            'div.q:nth-of-type(5)::text').extract_first() else ""
        item['school_type'] = response.css('div.z:nth-of-type(4)::text').extract_first().replace("：",
                                                                                                 "") if response.css(
            'div.z:nth-of-type(4)::text').extract_first() else ""
        item['school_mail'] = response.css('div.z:nth-of-type(6)::text').extract_first().replace("：",
                                                                                                 "") if response.css(
            'div.z:nth-of-type(6)::text').extract_first() else ""
        item['school_url'] = response.css('div.q a::text').extract_first()
        if response.css('div.z:nth-of-type(7)::text').extract_first():
            item['class_nums'] = response.css('div.z:nth-of-type(7)::text').extract_first().replace("：",
                                                                                                    "") if response.css(
                'div.z:nth-of-type(7)::text').extract_first() else ""
            item['school_address'] = response.css('div.z:nth-of-type(9)::text').extract_first().replace("：",
                                                                                                        "") if response.css(
                'div.z:nth-of-type(9)::text').extract_first() else ""
            item['postcode'] = response.css('div.z:nth-of-type(10)::text').extract_first().replace("：",
                                                                                                   "") if response.css(
                'div.z:nth-of-type(10)::text').extract_first() else ""
        else:
            item['school_address'] = response.css('div.z:nth-of-type(8)::text').extract_first().replace("：",
                                                                                                        "") if response.css(
                'div.z:nth-of-type(8)::text').extract_first() else ""
            item['postcode'] = response.css('div.z:nth-of-type(9)::text').extract_first().replace("：",
                                                                                                  "") if response.css(
                'div.z:nth-of-type(9)::text').extract_first() else ""
        item['school_desc'] = w3lib.html.remove_tags(response.css('div.jj').extract_first())
        yield item
