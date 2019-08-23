# -*- coding: utf-8 -*-
import scrapy
import csv
import json
import re
import time
from junyang_spider.items import BaiduSchoolItem


class BaiDuSchoolSpider(scrapy.Spider):
    name = "BaiDuSchool"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php",

    ]

    def __init__(self):
        super(BaiDuSchoolSpider, self).__init__()
        self.school_list = csv.reader(open('baidu_school.csv', 'r'))

    def start_requests(self):
        url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php"
        curriculum_list = [u'文科', u'理科', u'不分文理']
        batch_list = [u'提前批', u'一批', u'二批', u'三批', u'本科批', u'专科']
        for school in self.school_list:
            for batch in batch_list:
                for curriculum in curriculum_list:
                    data = {
                        'resource_id': '8306',
                        'format': 'json',
                        'ie': 'utf-8',
                        'oe': 'utf-8',
                        'query': school,
                        'from_mid': '1',
                        'tn': 'tangram',
                        'province': u'湖南',
                        'curriculum': curriculum,
                        'batch': batch,
                        '_': str(time.time()).replace(".", "")[:13],
                        'cb': 'jsonp2'
                    }
                    yield scrapy.FormRequest(url, formdata=data, method="GET")

    def parse(self, response):
        # print(response.body.decode())
        if response:
            content = re.search('jsonp\d\(((.|\n)*)\)', response.body.decode())
            result_dict = json.loads(content.group(1))
            rank_list = result_dict['data'][0]['disp_data']
            if rank_list:
                for rank in rank_list:
                    item = BaiduSchoolItem()
                    item['province'] = rank['province']
                    item['school'] = rank['school']
                    item['precedence'] = rank['precedence']
                    item['min'] = rank['min']
                    item['average'] = rank['average']
                    item['curriculum'] = rank['curriculum']
                    item['batch'] = rank['batch']
                    item['num'] = rank['num']
                    item['year'] = rank['year']
                    item['batchscore'] = rank['batchscore']
                    yield item
