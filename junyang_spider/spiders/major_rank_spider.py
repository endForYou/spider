# -*- coding: utf-8 -*-
import scrapy
import re
import w3lib.html
from junyang_spider.items import MajorRankItem


class MajorRankSpider(scrapy.Spider):
    name = "major_rank"
    allowed_domains = ["chinadegrees.cn"]
    start_urls = [
        "http://www.chinadegrees.cn/webrms/pages/Ranking/xkpmGXZJ2016.jsp",

    ]

    def parse(self, response):
        # print(response.css("a.hei14b"))
        for a in response.css("a.hei14b"):
            href = a.css("::attr('href')")
            major_big_type = a.css("::text").extract_first()
            data_dic = {
                'major_big_type': major_big_type
            }
            url = response.urljoin(href.extract_first())
            yield scrapy.Request(url, meta=data_dic, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for a in response.css("a.hei12"):
            href = a.css("::attr('href')")
            major_type_list = a.css("::text").extract_first().strip()
            major = re.split(r'\s+', major_type_list)
            major_type = major[1]
            major_code = major[0]
            data_dic = {
                'major_big_type': response.meta['major_big_type'],
                'major_type': major_type,
                'major_code': major_code
            }
            url = response.urljoin(href.extract_first())
            yield scrapy.Request(url, meta=data_dic, callback=self.parse_rank)

    def parse_rank(self, response):
        for td in response.css('td td td'):
            item = MajorRankItem()
            item['major_big_type'] = response.meta['major_big_type']
            item['major_type'] = response.meta['major_type']
            item['major_code'] = response.meta['major_code']
            rank_str = td.css("::text").extract_first().strip()
            if rank_str in ('A', 'A+', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-'):
                major_rank = td.css("::text").extract_first()
            else:
                item['major_rank'] = major_rank
                school = td.css("div::text").extract_first().strip()
                school_list = re.split(r'\s+', school)
                print(school_list)
                item['school_name'] = school_list[1]
                item['school_code'] = school_list[0]
                item['PKid'] = school_list[1] + " " + response.meta['major_type']
                yield item
