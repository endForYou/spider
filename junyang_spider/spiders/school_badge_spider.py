# -*- coding: utf-8 -*-
import scrapy
from junyang_spider.items import YouzySchoolBadgeItem


class SchoolBadgeSpider(scrapy.Spider):
    name = "school_badge"
    allowed_domains = ["youzy.cn"]
    start_urls = [
        "https://www.youzy.cn/college/search?page=1",
    ]
    custom_settings = {
        'ITEM_PIPELINES': {'gaokao.pipelines.SchoolBadgePipeline': 200}
    }

    def parse(self, response):
        for school in response.css("li.clearfix"):
            image_url = school.css('a img::attr("src")').extract_first()
            if image_url.find("http") != -1:
                item = YouzySchoolBadgeItem()
                item['school_name'] = school.css('a.name::text').extract_first()
                item['image_url'] = image_url
                yield item
        for i in range(2, 144):
            yield scrapy.Request('https://www.youzy.cn/college/search?page=%d' % i, callback=self.parse)
