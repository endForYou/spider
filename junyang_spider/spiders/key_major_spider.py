# -*- coding: utf-8 -*-
import scrapy
import re
import w3lib.html
from junyang_spider.items import KeyMajorItem


class KeyMajorSpider(scrapy.Spider):
    name = "KeyMajor"
    allowed_domains = ["cdgdc.edu.cn"]
    start_urls = [
        "http://www.cdgdc.edu.cn/xwyyjsjyxx/xwbl/zdjs/zdxk/zdxkmd/lsx/266612.shtml",

    ]

    def parse(self, response):
        #print(response.css("a.hei14b"))
        for a in response.css("p.Zmen2 a"):
            href = a.css("::attr('href')")
            big_type = a.css("::text").extract_first()
            data_dic = {
                'big_type': big_type
            }
            url = response.urljoin(href.extract_first())
            yield scrapy.Request(url, meta=data_dic, callback=self.parse_direct, dont_filter=True)


    def parse_direct(self, response):
        result = re.search("window.location='(.*)';", str(response.body))
        url = result.group(1)
        url = response.urljoin(url)
        data_dic = response.meta
        yield scrapy.Request(url, meta=data_dic, callback=self.parse_dir_contents, dont_filter=True)

    def parse_dir_contents(self, response):

        for a in response.css("td:nth-of-type(2) a"):
            href = a.css("::attr('href')")
            major_type_list = a.css("::text").extract_first().strip()
            major = re.split(r'\s+', major_type_list)
            type1 = major[1]
            code = str(major[0])
            data_dic = {
                'big_type': response.meta['big_type'],
                'type1': type1,
                'code': code
            }
            url = response.urljoin(href.extract_first())
            yield scrapy.Request(url, meta=data_dic, callback=self.parse_major, dont_filter=True)


    def parse_major(self, response):

        for td in response.css('tr:nth-of-type(n+2) td'):

            type2_str = td.css("p>span:nth-child(1)::text").extract_first()
            if type2_str in (u'一级学科', u"二级学科", None):
                #rows = int(td.css("::attr('rowspan')"))
                type2 = type2_str.strip() if type2_str else ""
            else:
                if re.search("\d", type2_str):
                    type3 = "".join(td.css("p>span::text").extract())
                else:
                    item = KeyMajorItem()
                    big_type = response.meta['big_type']
                    type1 = response.meta['type1']
                    code = response.meta['code']
                    item['big_type'] = big_type
                    item['type1'] = type1
                    item['code'] = code
                    item['type2'] = type2
                    item['type3'] = type3
                    school = td.css('p>span::text').extract_first()
                    item['school'] = school
                    yield item




