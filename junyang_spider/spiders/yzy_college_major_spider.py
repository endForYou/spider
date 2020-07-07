"""
@version:1.0
@author: endaqa
@file yzy_college_major_spider.py
@time 2020/3/23 13:48
"""

import scrapy
from junyang_spider.items import YzyCollegeMajorItem
import pymysql
from junyang_spider import settings


class YzyCollegeMajorSpider(scrapy.Spider):
    name = "yzy_college_major"
    allowed_domains = ["www.youzy.cn"]
    base_url = "https://www.youzy.cn"
    # start_urls = [
    #     "https://apigateway-toci.youzy.cn/Data/Colleges/Institutes/Get?collegeId=857",
    #     # "http://www.gaokaoq.com/major.html?level=2"
    #
    # ]
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyCollegeMajorPipline': 100},

    }

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
        sql = "select id,cid,name from college where cid is not NULL "
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def start_requests(self):
        colleges = self.get_colleges_from_db()
        # print(colleges)
        for college in colleges:
            college_id = college['id']
            college_name = college['name']
            yzy_college_id = college['cid']
            url = self.base_url + "/tzy/search/colleges/homepage/homePage?cid=" + str(yzy_college_id)
            data = {
                'college_id': college_id,
                'yzy_college_id': yzy_college_id,
                'college_name': college_name
            }
            yield scrapy.Request(url, meta=data, method="get", dont_filter=True)

    def parse(self, response):
        college_id = response.meta['college_id']
        college_name = response.meta['college_name']
        yzy_college_id = response.meta['yzy_college_id']
        # sid = response.meta['sid']
        for major in response.css("div.educational-major-list:nth-of-type(n+2) li"):
            major_name = major.css("::text").extract_first()
            if major_name.find("本") != -1:
                grade = 0
            else:
                grade = 1
            major_name = major_name.split("（")[0]
            item = YzyCollegeMajorItem()
            item['college_id'] = college_id
            item['college_name'] = college_name
            item['yzy_college_id'] = yzy_college_id
            item['grade'] = grade
            item['major_name'] = major_name
            yield item
