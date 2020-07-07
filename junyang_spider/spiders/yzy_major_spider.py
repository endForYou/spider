"""
@version:1.0
@author: endaqa
@file yzy_major_spider.py
@time 2020/3/16 11:16
"""
import scrapy
from junyang_spider.items import YzyMajorItem
from junyang_spider.items import YzyMajorDetailItem
import pymysql
from junyang_spider import settings


class YzyMajorSpider(scrapy.Spider):
    name = "yzy_major"
    allowed_domains = ["www.youzy.cn"]
    base_url = "https://www.youzy.cn"
    start_urls = [
        "https://www.youzy.cn/tzy/search/majors/homepage",
        # "http://www.gaokaoq.com/major.html?level=2"

    ]
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyMajorPipline': 100},

    }

    @classmethod
    def get_majors_from_db(cls):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        sql = "select * from yzy_major"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # def start_requests(self):
    #     majors = self.get_majors_from_db()
    #     # print(colleges)
    #     for major in majors:
    #         code = major['code']
    #         url = self.base_url + "/tzy/search/majors/smallMajor?code=%s" % code
    #         name = major['name']
    #         grade = major['grade']
    #         data = {
    #             "name": name,
    #             "grade": grade,
    #             "code": code
    #         }
    #         yield scrapy.Request(url, meta=data, method="get", callback=self.parse_detail)

    def parse(self, response):
        # 学校列表
        # sid = response.meta['sid']
        for e in response.css("div.bk-major-list.bkList div.content"):
            category_name_str = e.css("div.major-title>div.font::text").extract_first()
            category_name = category_name_str.split("（")[0]
            category_code = category_name_str.split("（")[1].split("）")[0]
            i = 1
            while True:
                sub_category = e.css("div.major-num:nth-of-type(%s)" % str(i + 1))
                # print(sub_category)
                # print(i)
                if not sub_category:
                    break
                sub_category_name_str = sub_category.css("a::text").extract_first()
                sub_category_name = sub_category_name_str.split("（")[0]
                sub_category_code = sub_category_name_str.split("（")[1].split("）")[0]
                major_list = e.css(" ul:nth-of-type(%s) a" % i)
                for major in major_list:
                    item = YzyMajorItem()
                    major_name = major.css("::text").extract_first()
                    major_code = major.css("::attr('href')").extract_first().split("code=")[1]
                    item['grade'] = 0
                    item['category_name'] = category_name
                    item['category_code'] = category_code
                    item['subcategory_name'] = sub_category_name
                    item['subcategory_code'] = sub_category_code
                    item['major_name'] = major_name
                    item['major_code'] = major_code
                    yield item
                i += 1
        for e in response.css("div.bk-major-list.zkList div.content"):
            category_name_str = e.css("div.major-title>div.font::text").extract_first()
            category_name = category_name_str.split("（")[0]
            category_code = category_name_str.split("（")[1].split("）")[0]
            i = 1
            while True:
                sub_category = e.css("div.major-num:nth-of-type(%s)" % str(i + 1))
                # print(sub_category)
                # print(i)
                if not sub_category:
                    break
                sub_category_name_str = sub_category.css("a::text").extract_first()
                sub_category_name = sub_category_name_str.split("(")[0]
                sub_category_code = sub_category_name_str.split("(")[1].split("）")[0]
                major_list = e.css(" ul:nth-of-type(%s) a" % i)
                for major in major_list:
                    item = YzyMajorItem()
                    major_name = major.css("::text").extract_first()
                    major_code = major.css("::attr('href')").extract_first().split("code=")[1]
                    item['grade'] = 1
                    item['category_name'] = category_name
                    item['category_code'] = category_code
                    item['subcategory_name'] = sub_category_name
                    item['subcategory_code'] = sub_category_code
                    item['major_name'] = major_name
                    item['major_code'] = major_code
                    yield item
                i += 1
        # college_level = e.css("div.top>a::attr('data-level')").extract_first()
        # college_name = e.css("div.top>a::text").extract_first()
        # province = e.css("li.quarter:nth-of-type(6)::text").extract_first()
        # # print(college_name)
        # item = YzyCollegeItem()
        # item['sid'] = sid
        # item['college_id'] = college_id
        # item['college_level'] = college_level
        # item['college_name'] = college_name
        # item['province'] = province
        # url = self.base_url + url
        #
        # yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        name = response.meta['name']
        grade = response.meta['grade']
        code = response.meta['code']
        item = YzyMajorDetailItem()
        item['grade'] = grade
        item['major_name'] = name
        item['major_code'] = code
        item['courses'] = response.css("#majorCourse::text").extract_first()
        item['description'] = response.css("#majorObjective::text").extract_first()
        item['employment'] = response.css("#employmentProspects::text").extract_first()
        item['knowledge'] = response.css("#majorLoreAndAbility::text").extract_first()
        item['inherit_secondary_vocational'] = None
        item['schooling_time'] = response.css(
            "div.col-xs-4:nth-of-type(2) p.major-overview-textMain::text").extract_first()
        item['degree'] = response.css("#majorLoreAndAbility::text").extract_first()
        # 专科
        if grade:
            item['job_qualification_certificate'] = response.css(
                ".introduce div:nth-of-type(4) p:nth-of-type(2)::text").extract_first()

            item['inherit_undergraduate'] = response.css("#progressions::text").extract_first()
            item['degree'] = None
        # 本科
        else:
            item['job_qualification_certificate'] = None
            item['inherit_undergraduate'] = None
            item['degree'] = response.css("div.col-xs-4:nth-of-type(3) p.major-overview-textMain::text").extract_first()
        yield item

    def parse_college_desc(self, response):
        item = response.meta['item']
        item['school_desc'] = response.css("#introduction::text").extract_first()
        yield item
