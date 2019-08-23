import scrapy
from junyang_spider.items import GkqItem


class GkqSpider(scrapy.Spider):
    name = "gaokaoq"
    allowed_domains = ["www.gaokaoq.com"]
    start_urls = [
        "http://www.gaokaoq.com/major.html?level=1",
        # "http://www.gaokaoq.com/major.html?level=2"

    ]

    def parse(self, response):
        for e in response.css("div.p-outer-title"):
            item = GkqItem()
            item['more_bigger_type'] = e.css("div.p-title::text").extract_first()
            for href in e.css("div.pro-msg a::attr('href')"):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, meta={'item': item}, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = response.meta['item']
        item['major_type'] = response.css('div.container.major-name.clearfix > div:nth-child(1) > h3::text').extract()
        item['profession'] = response.css(
            'body > div.container.clearfix > div.margin15.major-box.clearfix > div > div > a::text').extract()
        item['job_prospect'] = response.css(
            'body > div.container.clearfix > div:nth-child(2) > div > div:nth-child(2) > div.detail-box.detail-box2 > div').extract()
        yield item
