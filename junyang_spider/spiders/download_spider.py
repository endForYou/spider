"""
@version:1.0
@author: endaqa
@file download_spider.py
@time 2019/10/22 17:57
"""
"""
@version:1.0
@author: endaqa
@file paper_ewt360.py
@time 2019/10/15 10:46
"""
# -*- coding: utf-8 -*-
import scrapy
from junyang_spider.items import FileDownloadItem
import csv
# import pandas as pd


class DownloadSpider(scrapy.Spider):
    name = "download_spider"
    allowed_domains = ["ewt360.com"]
    # start_urls = [
    #     "https://www.ewt360.com/Review/Lists?page=1",
    # ]
    # custom_settings = {
    #     'ITEM_PIPELINES': {'junyang_spider.pipelines.PaperEWTPipeline': 200}
    # }
    # file = open("paper_file.csv", 'r', encoding='utf-8')
    #
    # csv_file = list(csv.reader(file))
    # df = pd.read_csv("paper_file.csv")

    def start_requests(self):
        print(self.df[1:100])
        for record in self.csv_file:
            print(record)
            url = record[6]
            url = url.replace("https:http", "https")
            if url.find('http') == -1 or url.find("Login") != -1:
                continue
            print(url)
            item = FileDownloadItem()
            item['file_urls'] = [url]
            yield item

    # def parse(self, response):
    #     item = FileDownloadItem()
    #     yield item
