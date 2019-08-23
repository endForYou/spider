# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from junyang_spider.items import GkcxCollegeEntryScoreItem


class GkcxEntryScoreSpider(scrapy.Spider):
    name = "gkcx_school_entry_score"
    allowed_domains = ["gkcx.eol.cn", "data-gkcx.eol.cn"]
    start_urls = [
        'https://data-gkcx.eol.cn/soudaxue/queryProvinceScore.html',
    ]

    def start_requests(self):
        url = self.start_urls[0]
        requests_header = {
            'Referer': 'https://gkcx.eol.cn/soudaxue/queryProvinceScore.html',
        }
        for i in range(1, 2594):
            data = {
                'messtype': 'jsonp',
                'callback': 'jQuery18306750020854009473_1530239221589',
                'provinceforschool': '',
                'schooltype': '',
                'page': str(i),
                'size': '50',
                'keyWord': '',
                'schoolproperty': '',
                'schoolflag': '',
                'province': '',
                'fstype': '',
                'zhaoshengpici': '',
                'fsyear': '',
                '_': str(time.time()).replace(".", "")[:13],
            }
            yield scrapy.FormRequest(url, formdata=data, method="GET", headers=requests_header)

    def parse(self, response):
        # print(response.body)
        # print(response.body.decode())
        content = re.search('_1530239221589\(((.|\n)*)\)', response.body.decode())
        result_dict = json.loads(content.group(1))
        school_list = result_dict['school']
        for school in school_list:
            item = GkcxCollegeEntryScoreItem()
            item['school_name'] = school['schoolname']
            item['enroll_place'] = school['localprovince']
            item['province'] = school['province']
            item['major_type'] = school['studenttype']
            item['years'] = school['year']
            item['enroll_batch'] = school['batch']
            item['average_score'] = school['var_score']
            item['line_difference'] = school['fencha']
            item['province_line'] = school['provincescore']
            item['min'] = school['min']
            if item:
                yield item
