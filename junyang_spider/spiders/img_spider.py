import scrapy

from junyang_spider.items import ImgsItem


class ImgSpider(scrapy.Spider):
    name = "img_spider"

    def start_requests(self):
        urls = [
            'http://zsxx.e21.cn/e21html/zsarticles/gaozhao/2022_08_15/81043.html',
            'http://zsxx.e21.cn/e21html/zsarticles/gaozhao/2022_08_15/81042.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contents = response.css('#zscontent p')
        for content in contents:
            item = ImgsItem()
            item['img_src'] = "http://zsxx.e21.cn"+content.css('a > img::attr("src")').extract_first()
            yield item
