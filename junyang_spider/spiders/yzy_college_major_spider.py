"""
@version:1.0
@author: endaqa
@file yzy_college_major_spider.py
@time 2020/3/23 13:48
"""

import scrapy
from junyang_spider.items import YzyMajorItem
import pymysql
from junyang_spider import settings


class YzyCollegeMajorSpider(scrapy.Spider):
    name = "yzy_college_major"
    allowed_domains = ["www.youzy.cn"]
    base_url = "https://apigateway-toci.youzy.cn"
    # start_urls = [
    #     "https://apigateway-toci.youzy.cn/Data/Colleges/Institutes/Get?collegeId=857",
    #     # "http://www.gaokaoq.com/major.html?level=2"
    #
    # ]
    # custom_settings = {
    #     'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyCollegeMajorPipline': 100},
    #
    # }

    @classmethod
    def get_colleges_from_db(cls):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        sql = "select college_id from college_yzy"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def start_requests(self):
        colleges = self.get_colleges_from_db()
        # print(colleges)
        for college in colleges:
            college_id = college['college_id']
            url = self.base_url + "/Data/Colleges/Institutes/Get?collegeId=" + str(college_id)
            yield scrapy.FormRequest(url, method="POST")

    def parse(self, response):
        print(response.text)
        # sid = response.meta['sid']
        # for e in response.css("div.bk-major-list.bkList div.content"):
        #     category_name_str = e.css("div.major-title>div.font::text").extract_first()
        #     category_name = category_name_str.split("（")[0]
        #     category_code = category_name_str.split("（")[1].split("）")[0]
        #     i = 1
        #     while True:
        #         sub_category = e.css("div.major-num:nth-of-type(%s)" % str(i + 1))
        #         # print(sub_category)
        #         # print(i)
        #         if not sub_category:
        #             break
        #         sub_category_name_str = sub_category.css("a::text").extract_first()
        #         sub_category_name = sub_category_name_str.split("（")[0]
        #         sub_category_code = sub_category_name_str.split("（")[1].split("）")[0]
        #         major_list = e.css(" ul:nth-of-type(%s) a" % i)
        #         for major in major_list:
        #             item = YzyMajorItem()
        #             major_name = major.css("::text").extract_first()
        #             major_code = major.css("::attr('href')").extract_first().split("code=")[1]
        #             item['grade'] = 0
        #             item['category_name'] = category_name
        #             item['category_code'] = category_code
        #             item['subcategory_name'] = sub_category_name
        #             item['subcategory_code'] = sub_category_code
        #             item['major_name'] = major_name
        #             item['major_code'] = major_code
        #             yield item
        #         i += 1
        # for e in response.css("div.bk-major-list.zkList div.content"):
        #     category_name_str = e.css("div.major-title>div.font::text").extract_first()
        #     category_name = category_name_str.split("（")[0]
        #     category_code = category_name_str.split("（")[1].split("）")[0]
        #     i = 1
        #     while True:
        #         sub_category = e.css("div.major-num:nth-of-type(%s)" % str(i + 1))
        #         # print(sub_category)
        #         # print(i)
        #         if not sub_category:
        #             break
        #         sub_category_name_str = sub_category.css("a::text").extract_first()
        #         sub_category_name = sub_category_name_str.split("(")[0]
        #         sub_category_code = sub_category_name_str.split("(")[1].split("）")[0]
        #         major_list = e.css(" ul:nth-of-type(%s) a" % i)
        #         for major in major_list:
        #             item = YzyMajorItem()
        #             major_name = major.css("::text").extract_first()
        #             major_code = major.css("::attr('href')").extract_first().split("code=")[1]
        #             item['grade'] = 1
        #             item['category_name'] = category_name
        #             item['category_code'] = category_code
        #             item['subcategory_name'] = sub_category_name
        #             item['subcategory_code'] = sub_category_code
        #             item['major_name'] = major_name
        #             item['major_code'] = major_code
        #             yield item
        #         i += 1
