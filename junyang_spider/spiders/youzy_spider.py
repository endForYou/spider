# -*- coding: utf-8 -*-
import scrapy
import w3lib.html
from junyang_spider.items import YouzyItem


class Youzy_Spider(scrapy.Spider):
    name = "youzy"
    allowed_domains = ["youzy.cn"]
    start_urls = [
        "https://www.youzy.cn/college/search?page=1",
        # "https://www.youzy.cn/college/848/home.html",

    ]

    def parse(self, response):
        for href in response.css("a.name::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_page)
            # all 141
            # 2,31
            # 32,61
            # 62 91
            # 92 121
            # 122 142
        for i in range(2, 144):
            yield scrapy.Request('https://www.youzy.cn/college/search?page=%d' % i, callback=self.parse)

    def parse_page(self, response):
        # item = YouzyItem()
        # item['school'] = w3lib.html.remove_tags(response.css("div.container-box.feature").extract_first())
        # yield item

        # # 清华大学
        # if response.css('table:nth-of-type(2) tr'):
        #     pass
        # for tr in response.css("li tr:nth-of-type(n+2)"):
        #     item = YouzyItem()
        #
        #     departure = tr.css("td:nth-child(1)::text").extract_first().strip()
        #     div_text = tr.css("td:nth-child(2)>div::text").extract_first()
        #     td_text = tr.css("td:nth-child(2)::text").extract_first()
        #     if div_text:
        #         major = div_text.strip()
        #     elif td_text:
        #         major = td_text.strip()
        #     else:
        #         major = ""
        #     item['departure'] = departure
        #     item['major'] = major
        #     print(item)
        school = response.css('h2::text').extract_first().strip()
        for tr in response.css('div.container.index>div:nth-of-type(3) tr'):

            td_text_list = [td_text for td_text in tr.css("td").extract() if td_text.find(u'学部') == -1]
            td_text_list = [w3lib.html.remove_tags(x) for x in td_text_list]
            td_list_len = len(td_text_list)
            flag1, flag2 = False, False
            if td_text_list and td_list_len >= 2:
                for td_text in td_text_list:
                    if td_text.find(u'院') != -1:
                        flag1 = True
                    elif td_text.find(u'系') != -1:
                        flag2 = True
                if (flag1 and not flag2) or (flag2 and not flag1):
                    if td_text_list[td_list_len - 1].find(u'院') != -1 or td_text_list[td_list_len - 1].find(u'系') != -1:
                        td_text_list[0], td_text_list[td_list_len - 1] = td_text_list[td_list_len - 1], td_text_list[0]
                el = "\n".join(td_text_list)
                if el and (el.find(u'专业') != -1 or el.find(u'学院') != -1 or el.find(u'系') != -1):
                    item = YouzyItem()
                    item['school'] = school
                    item['major'] = el
                    # print(item)
                    yield item
