"""
@version:1.0
@author: endaqa
@file yzy_enroll_guide_spider.py
@time 2020/4/13 14:45
"""

import scrapy
from junyang_spider.items import YzyEnrollGuideItem
from hashlib import md5
import pymysql
from junyang_spider import settings


class YzyMajorSpider(scrapy.Spider):
    name = "yzy_enroll_guide"
    allowed_domains = ["www.youzy.cn"]
    base_url = "https://www.youzy.cn"
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyEnrollGuidePipline': 100},

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
        sql = "select id,cid from college where cid is not NULL and id >2520 "
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def get_all_existed_enroll_guides(cls):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        sql = "select title from enroll_guide  "
        cursor.execute(sql)
        result = cursor.fetchall()
        existed_guides = []
        for data in result:
            title = data['title']
            title_new = md5(title.encode("utf-8")).hexdigest()
            existed_guides.append(title_new)
        return existed_guides

    def start_requests(self):
        colleges = self.get_colleges_from_db()
        # print(colleges)
        for college in colleges:
            cid = college['cid']
            college_id = college['id']
            url = self.base_url + "/tzy/search/colleges/homepage/newsList?cid=%s" % cid
            data = {
                "college_id": college_id
            }
            yield scrapy.Request(url, meta=data, method="get", dont_filter=True)

    def parse(self, response):
        # 学校列表
        college_id = response.meta['college_id']
        existed_guides = self.get_all_existed_enroll_guides()
        for e in response.css("div.news-list"):
            publish_date = e.css("div.date::text").extract_first() + "-01"
            for li in e.css("div.list>ul li"):
                title = li.css("a::attr('title')").extract_first()
                title_new = md5(title.encode("utf-8")).hexdigest()
                if title_new in existed_guides:
                    continue
                # item = YzyEnrollGuideItem()
                # href = li.css("a::attr('href')").extract_first()
                # item['college_id'] = college_id
                # item['title'] = title
                #
                # item['publish_date'] = publish_date
                # url = self.base_url + href
                # yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail, dont_filter=True)
                if publish_date.find("2020") != -1 or title.find("2020") != -1:
                    item = YzyEnrollGuideItem()
                    href = li.css("a::attr('href')").extract_first()
                    item['college_id'] = college_id
                    item['title'] = title

                    item['publish_date'] = publish_date
                    url = self.base_url + href
                    yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta['item']

        item['content'] = response.css("div.content").extract_first()
        if item['content']:
            yield item
