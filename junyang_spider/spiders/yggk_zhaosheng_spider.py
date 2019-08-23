# -*- coding: utf-8 -*-
import scrapy
import w3lib.html
from junyang_spider.items import YGGKZhaoShengItem


class YggkZhaoShengSpider(scrapy.Spider):
    name = "yggk_zhaosheng"
    allowed_domains = ["gaokao.chsi.com.cn"]
    start_urls = [
        "http://gaokao.chsi.com.cn/zsgs/zhangcheng/listVerifedZszc--method-index,lb-1,ssdm-00,start-0.dhtml",

    ]

    def parse(self, response):

        for href in response.css("td.yes a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        for i in range(100, 2721, 100):
            yield scrapy.Request(
                'http://gaokao.chsi.com.cn/zsgs/zhangcheng/listVerifedZszc--method-index,lb-1,ssdm-00,start-' + str(
                    i) + '.dhtml'
                , callback=self.parse)

    def parse_dir_contents(self, response):
        # item = Yggk_ZhaoSheng_Item()
        # zhaosheng_str = response.css('div.width1000.gery > h2::text').extract_first()
        # item['school_name'] = zhaosheng_str.split(u"招生章程")[0]
        no_info = response.css(
            'div.width1000.gery > div.zszcdel:nth-child(3) >div.right>div.noInfoTxt::text').extract_first()
        no_info_2017 = response.css(
            'div.width1000.gery > div.zszcdel:nth-child(4) >div.right>div.noInfoTxt::text').extract_first()
        href_2017 = response.css(
            "div.width1000.gery > div.zszcdel:nth-child(4) >div.right a:nth-child(1)::attr('href')")
        url_2017 = response.urljoin(href_2017.extract_first())
        if no_info and no_info_2017:
            item = YGGKZhaoShengItem()
            zhaosheng_str = response.css('div.width1000.gery > h2::text').extract_first()
            item['school_name'] = zhaosheng_str.split(u"招生章程")[0]
            item['enrollment_guide_of_2018'] = ""
            item['enrollment_guide_of_2017'] = ""
            yield item
        # if no_info:
        #     item['enrollment_guide_of_2018'] = ""
        #     yield scrapy.Request(url_2017, meta={'item': item}, callback=self.parse_zhaosheng_2017_desc)
        #
        # else:
        #     href_2018 = response.css("div.width1000.gery > div.zszcdel:nth-child(3) >div.right a::attr('href')")
        #     url_2018 = response.urljoin(href_2018.extract_first())
        #     data_dict = {'item': item,
        #                  'url_2017': url_2017}
        #     yield scrapy.Request(url_2018, meta=data_dict, callback=self.parse_zhaosheng_2018_desc)

    def parse_zhaosheng_2018_desc(self, response):
        item = response.meta['item']
        url_2017 = response.meta['url_2017']
        item['enrollment_guide_of_2018'] = w3lib.html.remove_tags(response.css('div.content').extract_first())
        yield scrapy.Request(url_2017, meta={'item': item}, callback=self.parse_zhaosheng_2017_desc)

    def parse_zhaosheng_2017_desc(self, response):
        item = response.meta['item']
        item['enrollment_guide_of_2017'] = w3lib.html.remove_tags(response.css('div.content').extract_first())
        yield item
