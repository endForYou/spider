"""
@version:1.0
@author: endaqa
@file yzy_college_enroll_code_spider.py
@time 2020/3/3 17:37
"""
import scrapy
from junyang_spider.items import YzyCollegeEnrollCodeItem
import pymysql
from junyang_spider import settings
import json
from junyang_spider.libs import yzy
from junyang_spider.libs import execute_js


class YzyCollegeEnrollCodeSpider(scrapy.Spider):
    name = "yzy_college_enroll_code"
    allowed_domains = ["youzy.cn"]
    base_url = "https://ia-pv4y.youzy.cn"
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyCollegeEnrollCodePipline': 100},

    }

    @classmethod
    def get_provinces_from_db(cls):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        sql = "select ProvinceId from yzy_province"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        connect.close()
        return result

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
        cursor.close()
        connect.close()
        return result

    def start_requests(self):
        # provinces = self.get_provinces_from_db()
        colleges = self.get_colleges_from_db()
        # print(colleges)
        province_list = [839, 849]
        for province_id in province_list:
            for college in colleges:
                college_id = college['college_id']
                url = self.base_url + "/Data/ScoreLines/UCodes/QueryList"
                data = {
                    'provinceId': str(province_id),
                    'collegeId': str(college_id)
                }
                encrypted_hex = execute_js.encrypt_data(data)
                data = {
                    'data': encrypted_hex
                }
                # print(data, college_id, province_id)
                yield scrapy.FormRequest(url, method="POST", formdata=data)
                # yield scrapy.FormRequest(url, method="POST", formdata=data)

    def parse(self, response):
        # 学校列表
        # print(response.text)
        infos = json.loads(response.text)['result']
        for info in infos:
            # meta = response.meta
            item = YzyCollegeEnrollCodeItem()
            item['provinceId'] = info['provinceId']
            item['provinceName'] = info['provinceName']
            item['uCodeNum'] = info['uCodeNum']
            item['admissCode'] = info['admissCode']
            item['collegeId'] = info['collegeId']
            item['collegeName'] = info['collegeName']
            item['sort'] = info['sort']
            item['isOld'] = info['isOld']
            item['codeChangeYear'] = info['codeChangeYear']
            item['str_id'] = info['id']
            yield item
