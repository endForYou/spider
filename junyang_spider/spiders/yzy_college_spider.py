"""
@version:1.0
@author: endaqa
@file yzy_college_spider.py
@time 2020/2/12 10:40
"""
import scrapy
from junyang_spider.items import YzyCollegeItem


class YzyCollegeSpider(scrapy.Spider):
    name = "yzy_college"
    allowed_domains = ["www.youzy.cn"]
    base_url = "https://www.youzy.cn"
    start_urls = [
        "https://www.youzy.cn/tzy/search/colleges/collegeList",
        # "http://www.gaokaoq.com/major.html?level=2"

    ]
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyCollegePipeline': 100},

    }

    def start_requests(self):
        for page in range(1, 146):
            url = self.base_url + "/tzy/search/colleges/collegeList?page=" + str(page)

            yield scrapy.Request(url, meta={"sid": page}, method="GET", dont_filter=True)

    def parse(self, response):
        # 学校列表
        sid = response.meta['sid']
        for e in response.css("li.clearfix"):
            url = e.css("div.top>a::attr('href')").extract_first()
            college_id = e.css("div.top>a::attr('data-num')").extract_first()
            college_level = e.css("div.top>a::attr('data-level')").extract_first()
            college_name = e.css("div.top>a::text").extract_first()
            province = e.css("li.quarter:nth-of-type(6)::text").extract_first()
            # print(college_name)
            item = YzyCollegeItem()
            item['sid'] = sid
            item['college_id'] = college_id
            item['college_level'] = college_level
            item['college_name'] = college_name
            item['province'] = province
            url = self.base_url + url

            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta['item']
        print(item)
        item['creation_time'] = response.css("p.creation::text").extract_first()
        item['is_public'] = response.css("p.type::text").extract_first()
        item['school_type'] = response.css("p.classify::text").extract_first()
        item['belong_to'] = response.css("p.belong::text").extract_first()
        item['is_undergraduate'] = response.css("p.education::text").extract_first()
        item['address'] = response.css("p.cityName::text").extract_first().strip()
        item['master_station_count'] = response.css("p.pointsOfShuo::text").extract_first() if response.css(
            "p.pointsOfShuo::text") else None
        item['doctor_station_count'] = response.css("p.pointsOfBo::text").extract_first() if response.css(
            "p.pointsOfBo::text") else None
        if not response.css("p a::attr('href')"):
            url = response.css(".text-right a::attr('href')").extract_first()
        else:
            url = response.css("p a::attr('href')").extract_first()
        url = self.base_url + url
        yield scrapy.Request(url, meta={'item': item}, callback=self.parse_college_desc, dont_filter=True)

    def parse_college_desc(self, response):
        item = response.meta['item']
        item['school_desc'] = response.css("#introduction::text").extract_first()
        yield item
