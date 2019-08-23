# -*- coding: utf-8 -*-
import scrapy
import w3lib.html
import json
from junyang_spider.items import YGGKItem


class YggkSpider(scrapy.Spider):
    name = "yangguang_gaokao"
    allowed_domains = ["gaokao.chsi.com.cn"]
    start_urls = [
        # "http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-0.dhtml",
        # "http://gaokao.chsi.com.cn/sch/schoolInfoMain--schId-1.dhtml",
        # "http://gaokao.chsi.com.cn/sch/search.do?searchType=1&yxmc=&zymc=&sySsdm=&ssdm=43&yxls=&yxlx=&xlcc=bk&zgsx=985",
        "http://gaokao.chsi.com.cn/sch/search.do?searchType=1&start=0",

    ]

    def parse(self, response):

        for tr in response.css("div.yxk-table>table tr"):
            item = YGGKItem()
            temp_url = tr.css("td.js-yxk-yxmc>a::attr('href')").extract_first()
            if temp_url:
                url = response.urljoin(temp_url)
                item['school_name'] = tr.css('td:nth-child(1)>a::text').extract_first().strip() if tr.css(
                    'td:nth-child(1)>a::text').extract_first() else ""
                item['school_location'] = tr.css('td:nth-child(2)::text').extract_first().strip() if tr.css(
                    'td:nth-child(2)::text').extract_first() else ""
                item['school_type'] = tr.css('td:nth-child(4)::text').extract_first().strip() if tr.css(
                    'td:nth-child(4)::text').extract_first() else ""
                item['education_level'] = tr.css('td:nth-child(5)::text').extract_first().strip() if tr.css(
                    'td:nth-child(5)::text').extract_first() else ""
                item['school_feature'] = tr.css('td:nth-child(6)>span::text').extract_first().strip() if tr.css(
                    'td:nth-child(6)>span::text').extract_first() else ""
                yield scrapy.Request(url, meta={'item': item}, callback=self.parse_dir_contents)
        for i in range(20, 2681, 20):
            yield scrapy.Request("http://gaokao.chsi.com.cn/sch/search.do?searchType=1&start=%d" % i,
                                 callback=self.parse)

    def parse_dir_contents(self, response):
        item = response.meta['item']
        # item = Yangguang_Gaokao_Item()
        school_url = w3lib.html.remove_tags(response.css(
            'div.yxk-col.yxk-yxmsg.clearfix>div.mid>div.msg:nth-child(1)>span:nth-child(2)').extract_first())
        item['school_url'] = school_url.strip() if school_url else ""
        school_address = response.css(
            'div.yxk-col.yxk-yxmsg.clearfix>div.mid>div:nth-child(2)>span::text').extract_first()

        item['school_address'] = school_address.strip() if school_address else ""
        # 学校简介
        school_desc_url = response.urljoin(
            response.css("div.nav-container a:nth-of-type(2)::attr('href')").extract()[0])
        # 专业介绍
        major_desc_url = response.urljoin(
            response.css("div.nav-container a:nth-of-type(4)::attr('href')").extract()[0])
        # 奖学金
        scholarship_url = response.urljoin(
            response.css("div.nav-container a:nth-of-type(7)::attr('href')").extract()[0])
        # # 食宿条件
        food_and_stay_condition_url = response.urljoin(
            response.css("div.nav-container a:nth-of-type(8)::attr('href')").extract()[0])
        # yield scrapy.Request(food_and_stay_condition_url, meta={'item': item},
        #                      callback=self.parse_food_and_stay_condition)
        # 毕业生就业
        student_employment_url = response.urljoin(
            response.css("ul.nav-more-list>li:nth-child(4)>a::attr('href')").extract()[0])
        # yield scrapy.Request(student_employment_url, meta={'item': item}, callback=self.parse_student_employment)
        # 基础设施
        infrastructure_url = response.urljoin(
            response.css("ul.nav-more-list>li:nth-child(5)>a::attr('href')").extract()[0])
        data_dict = {'item': item,
                     'major_desc_url': major_desc_url,
                     'scholarship_url': scholarship_url,
                     'food_and_stay_condition_url': food_and_stay_condition_url,
                     'student_employment_url': student_employment_url,
                     'infrastructure_url': infrastructure_url}
        # yield scrapy.Request(infrastructure_url, meta={'item': item}, callback=self.parse_infrastructure)

        yield scrapy.Request(school_desc_url, meta=data_dict, callback=self.parse_school_desc)

        # yield scrapy.Request(major_desc_url, meta={'item': item}, callback=self.parse_major_desc)

    def parse_school_desc(self, response):
        item = response.meta['item']
        major_desc_url = response.meta['major_desc_url']
        item['school_desc'] = w3lib.html.remove_tags(response.css('div.container').extract_first()).strip()
        yield scrapy.Request(major_desc_url, meta=response.meta, callback=self.parse_major_desc)

    def parse_scholarship(self, response):
        item = response.meta['item']
        item['scholarship'] = w3lib.html.remove_tags(response.css('div.container').extract_first()).strip()
        yield scrapy.Request(response.meta['food_and_stay_condition_url'], meta=response.meta,
                             callback=self.parse_food_and_stay_condition)

    def parse_food_and_stay_condition(self, response):
        item = response.meta['item']
        item['food_and_stay_condition'] = w3lib.html.remove_tags(response.css('div.container').extract_first()).strip()

        yield scrapy.Request(response.meta['student_employment_url'], meta=response.meta,
                             callback=self.parse_student_employment)

    def parse_student_employment(self, response):
        item = response.meta['item']
        item['student_employment'] = w3lib.html.remove_tags(response.css('div.yxk-detail-con').extract_first()).strip()

        yield scrapy.Request(response.meta['infrastructure_url'], meta=response.meta,
                             callback=self.parse_infrastructure)

    def parse_infrastructure(self, response):
        item = response.meta['item']
        item['infrastructure'] = w3lib.html.remove_tags(response.css('div.yxk-detail-con').extract_first()).strip()

        yield item

    def parse_major_desc(self, response):
        item = response.meta['item']
        major_big_type_list = response.css(
            'div.container>div:nth-child(3) > div.ch-tab.clearfix:nth-child(1)>div>a::text').extract()
        major_type = response.css('div.container >div:nth-child(3)>div.tab-content')
        item['major_desc'] = dict()
        for i in range(0, len(major_big_type_list)):
            major_type_list = major_type.css('div:nth-child(' + str(i + 1) + ')>ul>li')
            item['major_desc'][major_big_type_list[i]] = []
            for e in major_type_list:
                if e.css('a'):
                    element = e.css('a::text').extract_first().strip().replace('\r\n', '').replace(' ', '').replace(
                        '\n', '')

                    item['major_desc'][major_big_type_list[i]].append(element)
                else:
                    element = e.css('::text').extract_first().strip().replace('\r\n', '').replace(' ', '').replace(
                        '\n', '')
                    item['major_desc'][major_big_type_list[i]].append(element)

        item['major_desc'] = json.dumps(item['major_desc'], indent=2, ensure_ascii=False)
        yield scrapy.Request(response.meta['scholarship_url'], meta=response.meta, callback=self.parse_scholarship)
