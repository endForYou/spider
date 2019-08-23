"""
@version:1.0
@author: endaqa
@file college_spider.py
@time 2019/8/21 17:27
"""
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from junyang_spider.items import SchoolItem


class CollegeSpider(CrawlSpider):
    name = 'college'
    allowed_domains = ['zsc.ynnu.edu.cn/articlelist.aspx?id=43']
    start_urls = ['https://zsw.bjtu.edu.cn/list/index/id/37.html']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def parse(self, response):
        item = SchoolItem()
        ti = response.xpath('//*[@id="condition-province"]/li/a/text()').extract()
        t2 = response.xpath("//*[@id='condition-year']/li/a/text()").extract()
        t3 = response.xpath( "//*[@id='condition-type']/li[1]/a/text()").extract()
        t4 = response.xpath("//*[@id='condition-sort']/li/a/text()").extract()
        t5 = response.xpath("//*[@id='condition-school']/li/a/text()").extract()
        print(ti,t2,t3,t4,t5)
        data = response.xpath('//*[@id="one-year-table"]/tbody')
        for i in data:

            a  = i.xpath('//tr[1]//text()').extract()
            print(a)
        # i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()

        #return i
