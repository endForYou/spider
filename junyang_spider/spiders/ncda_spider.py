"""
@version:1.0
@author: endaqa
@file ncda_spider.py
@time 2019/11/7 18:27
"""

import scrapy
from junyang_spider.items import NcdaItem


# import csv
# import pandas as pd


class NCDASpider(scrapy.Spider):
    name = "ncda_spider"
    allowed_domains = ["ncda.org"]
    start_urls = [
        "https://www.ncda.org/aws/NCDA/pt/sp/CC_home_page",
    ]

    # custom_settings = {
    #     'ITEM_PIPELINES': {'junyang_spider.pipelines.PaperEWTPipeline': 200}
    # }
    # file = open("paper_file.csv", 'r', encoding='utf-8')
    #
    # csv_file = list(csv.reader(file))
    # df = pd.read_csv("paper_file.csv")

    # def start_requests(self):
    #
    #     for i in range(1, 9):
    #         selector = "#tabs-%s a.viewall::attr('href')" % i
    #         print(record)
    #         url = record[6]
    #         url = url.replace("https:http", "https")
    #         if url.find('http') == -1 or url.find("Login") != -1:
    #             continue
    #         print(url)
    #         item = FileDownloadItem()
    #         item['file_urls'] = [url]
    #         yield item

    def parse(self, response):
        for i in range(1, 9):
            div = response.css("div#tabs-%s" % i)
            url = div.css("a.viewall::attr('href')").extract_first()
            category = div.css("h2::text").extract_first()
            data_dict = {
                'category': category
            }
            yield scrapy.Request(url, meta=data_dict, callback=self.parse_list)

    def parse_list(self, response):
        links = response.css("a.tcs_details_link")
        data_dict = response.meta
        for link in links:
            url = link.css("::attr('href')").extract_first()
            yield scrapy.Request(url, meta=data_dict, callback=self.pass_content)

    def pass_content(self, response):

        content = response.css("div.tcs-news-content").extract_first()
        public_date = response.css("h4::text").extract_first()
        title = response.css("h2.tcsDetails::text").extract_first()
        author = response.css("h3.tcsDetails::text").extract_first()
        category = response.meta['category']
        item = NcdaItem()
        item['content'] = content
        item['public_date'] = public_date
        item['title'] = title
        item['author'] = author
        item['category'] = category
        return item
