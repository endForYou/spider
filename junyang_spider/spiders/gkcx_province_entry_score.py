# -*- coding: utf-8 -*-
import scrapy
import w3lib.html
import json
import re
from junyang_spider.items import EOLEntryScoreItem


class Gkcx_Entry_Score_Spider(scrapy.Spider):
    name = "gkcx_province_entry_score"
    allowed_domains = ["gkcx.eol.cn", "data-gkcx.eol.cn"]
    start_urls = [
        "https://data-gkcx.eol.cn/soudaxue/queryProvince.html?messtype=jsonp&callback=jQuery18308323446087692192_1527841553248&luqutype3=&province3=&year3=&luqupici3=&page=1&size=50&_=1527841553762",

    ]

    def parse(self, response):
        # print(response.body.decode())
        content = re.search('_1527841553248\(((.|\n)*)\)', response.body.decode())
        result_dict = json.loads(content.group(1))
        school_list = result_dict['school']
        for school in school_list:
            item = EOLEntryScoreItem()
            item['province'] = school['province']
            item['major_type'] = school['type']
            item['years'] = school['year']
            item['batch'] = school['bath']
            item['rank_line'] = school['score']
            yield item
            # 2,1001
        for i in range(2, 36):
            yield scrapy.Request(
                "https://data-gkcx.eol.cn/soudaxue/queryProvince.html?messtype=jsonp&callback=jQuery18308323446087692192_1527841553248&luqutype3=&province3=&year3=&luqupici3=&page=%d&size=50&_=1527841553762" % i,
                callback=self.parse)
