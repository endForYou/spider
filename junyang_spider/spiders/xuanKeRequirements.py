import scrapy
from junyang_spider.items import XuanKeRequirementsItem


class XuanKeRequirements(scrapy.Spider):
    name = "xuanke"
    allowed_domains = ["zjzs.net", ]
    start_urls = [
        "http://zt.zjzs.net/xk2019/allcollege.html",

    ]

    def parse(self, response):

        for tr in response.css("tr:nth-of-type(n+2)"):
            if tr.css("td:nth-of-type(3)::text").extract_first():
                item = dict()
                item['url'] = tr.css("td:nth-of-type(4)>a::text").extract_first()
                item['area'] = tr.css("td:nth-of-type(1)::text").extract_first()
                item['school_code'] = tr.css("td:nth-of-type(2)::text").extract_first()
                item['school_name'] = tr.css("td:nth-of-type(3)::text").extract_first()
                href = tr.css("td:nth-of-type(5) > a::attr('href')").extract_first()
                url = response.urljoin(href)
                data_dict = {
                    'item': item,
                }
                yield scrapy.Request(url, meta=data_dict, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = response.meta['item']
        for tr in response.css('tr:nth-of-type(n+2)'):
            if tr.css('td:nth-of-type(1)::text').extract_first():
                requirements_item = XuanKeRequirementsItem()
                requirements_item['url'] = item['url']
                requirements_item['area'] = item['area']
                requirements_item['school_code'] = item['school_code']
                requirements_item['school_name'] = item['school_name']
                requirements_item['level'] = tr.css("td:nth-of-type(1)::text").extract_first()
                requirements_item['major_name'] = tr.css("td:nth-of-type(2)::text").extract_first()
                requirements_item['requirements'] = tr.css("td:nth-of-type(4)::text").extract()
                requirements_item['major_in'] = tr.css("td:nth-of-type(5)::text").extract()
                yield requirements_item
