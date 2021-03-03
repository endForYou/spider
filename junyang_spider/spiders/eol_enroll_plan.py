"""
@version:1.0
@author: endaqa
@file eol_enroll_plan.py
@time 2020/8/3 17:48
"""

import scrapy
import json
import re
from junyang_spider.items import EolEntryScoreItem


class EntryEnrollPlan(scrapy.Spider):
    name = "eol_enroll_plan"
    allowed_domains = ["eol.cn", ]
    start_urls = [
        "http://www.eol.cn/e_html/gk/zszc/index.shtml",

    ]

    def parse(self, response):
        # print(response.body.decode())
        content = re.search('_1528102898126\(((.|\n)*)\)', response.body.decode())
        result_dict = json.loads(content.group(1))
        school_list = result_dict['school']
        for school in school_list:
            item = EolEntryScoreItem()
            item['school_name'] = school['schoolname']
            item['major_name'] = school['specialtyname']
            item['enroll_place'] = school['localprovince']
            item['major_type'] = school['studenttype']
            item['years'] = school['year']
            item['enroll_batch'] = school['batch']
            item['average_score'] = school['var_score']
            yield item
            # 2,1001
        for i in range(2, 1262):
            yield scrapy.Request(
                "https://data-gkcx.eol.cn/soudaxue/querySpecialtyScore.html?messtype=jsonp&callback=jQuery18307972060040650979_1528102898126&provinceforschool=%E7%A6%8F%E5%BB%BA&schooltype=&page=" + str(
                    i) + "&size=50&keyWord=&schoolproperty=&schoolflag=&province=&fstype=&zhaoshengpici=&fsyear=&zytype=&_=1528102898549",
                callback=self.parse)
