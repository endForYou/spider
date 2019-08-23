import scrapy
from junyang_spider.items import GkItem


class GaokaoSpider(scrapy.Spider):
    name = "gaokao"
    allowed_domains = ["www.diyigaokao.com", "http://www.gaokaoq.com/"]
    start_urls = [
        # "http://www.diyigaokao.com/major/",
        "http://www.diyigaokao.com/major/zk/",
        # "http://www.gaokaoq.com/major.html?level=1",
        # "http://www.gaokaoq.com/major.html?level=2",

    ]

    def parse(self, response):

        for href in response.css("div.list a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)
            # title = sel.xpath('a/text()').extract()
            # link = sel.xpath('a/@href').extract()
            # desc = sel.xpath('text()').extract()
            # print title, link, desc

    def parse_dir_contents(self, response):
        item = GkItem()
        item['name_of_major'] = response.css('div.searchSpecalty-result-intro ul>li:nth-child(1)::text').extract()
        item['subject'] = response.css('div.searchSpecalty-result-intro ul>li:nth-child(2)::text').extract()
        item['type'] = response.css('div.searchSpecalty-result-intro ul>li:nth-child(3)::text').extract()
        item['major_code'] = response.css('div.searchSpecalty-result-intro ul>li:nth-child(4)::text').extract()
        details = response.css('div.details')

        item['career_can_be'] = details.css('ol:nth-child(2)').css('li::text').extract()
        item['similar_major'] = details.css('ol:nth-child(4)').css('li>a::text').extract() + \
                                details.css('ol:nth-child(4)').css('li::text').extract()
        div = details.css('#J-searchSpecaltly-intro > div > div').extract()
        p = details.css('#J-searchSpecaltly-intro > div > p').extract()
        if p:
            item['major_desc'] = p
        elif div:
            item['major_desc'] = div
        else:
            item['major_desc'] = ""
        yield item
