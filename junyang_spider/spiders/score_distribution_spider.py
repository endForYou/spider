# -*- coding: utf-8 -*-
import scrapy
from junyang_spider.items import ScoreDistributionItem


class ScoreDistribution(scrapy.Spider):
    name = "score_distribution"
    allowed_domains = ["gaokw.com"]
    start_urls = [
        "http://www.gaokw.com/gaokao/guizhou/168385.html",

    ]

    def parse(self, response):
        # print(response.css("a.hei14b"))
        column = 4
        items = response.css('div.yplist tr')
        # print(items)
        line = 0
        buf = []
        for item in items:
            # print(item)
            if line < column:
                buf.append(item)
                line = line + 1
            if line == column:
                item_obj = ScoreDistributionItem()
                for (a, b, c, d) in zip(buf[0].css('td'), buf[1].css('td'), buf[2].css('td'), buf[3].css('td')):
                    item_obj['score'] = "".join(a.css('::text').extract())
                    item_obj['people'] = b.css('::text').extract_first()
                    item_obj['accumulative_people'] = c.css('::text').extract_first()
                    item_obj['accumulative_rate'] = d.css('::text').extract_first()
                    if item_obj['score'].find(u'各段分数') == -1 and item_obj['accumulative_people'] is not None \
                            and item_obj['accumulative_people'] != '\xa0':
                        yield item_obj
                    # if ",".join(item_obj).find(u'各段分数') == -1 or "".join(item_obj):
                    #     print(item_obj)
                    #
                    # else:
                    #     continue
                line = 0
                buf = []
