"""
@version:1.0
@author: endaqa
@file yzy_major_scoreline_spider.py
@time 2020/3/4 17:56
"""
import scrapy
from junyang_spider.items import YzyEnrollPlanItem
import pymysql
from junyang_spider import settings
import json
from junyang_spider.libs import execute_js, yzy


class YzyEnrollPlanSpider(scrapy.Spider):
    name = "yzy_enroll_plan"
    allowed_domains = ["youzy.cn"]
    base_url = "https://ia-pv4y.youzy.cn"
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyEnrollPlanPipline': 100},

    }

    @classmethod
    def get_colleges_enroll_code_from_db(cls):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        sql = "select provinceId,uCodeNum from yzy_college_enroll_code "
        #sql = "select provinceId,uCodeNum from yzy_college_enroll_code where uCodeNum='43_1772_0_0'"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        connect.close()
        return result

    def start_requests(self):
        college_enroll_codes = self.get_colleges_enroll_code_from_db()
        # print(colleges)
        for college_enroll_code in college_enroll_codes:
            province_id = college_enroll_code['provinceId']
            ucode = college_enroll_code['uCodeNum']
            url = self.base_url + "/Data/ScoreLines/Plans/Professions/Query"
            year = 2019
            data = {
                'year': year,
                'ucodes': ucode

            }
            encrypted_hex = execute_js.encrypt_data(data)
            #print(encrypted_hex)
            data = {
                'data': encrypted_hex
            }
            # print(data, college_id, province_id)
            meta_data = {
                'province_id': province_id
            }

            yield scrapy.FormRequest(url, meta=meta_data, method="POST", formdata=data)

    def parse(self, response):
        # 招生计划列表
        # print(response.text)
        print(response.text)
        province_id = response.meta['province_id']
        infos = json.loads(response.text)['result']['plans']
        for info in infos:
            # meta = response.meta
            item = YzyEnrollPlanItem()
            item['year'] = info['year']
            # 只要2016及以后的数据
            item['courseType'] = info['courseType']
            item['batch'] = info['batch']
            item['batchName'] = info['batchName']
            item['uCode'] = info['uCode']
            item['majorCode'] = info['majorCode']
            item['professionName'] = yzy.show_str(info['professionName']) if info['professionName'] else None
            item['professionCode'] = yzy.show_str(info['professionCode']) if info['professionCode'] else None
            item['planNum'] = yzy.show_number(info['planNum']) if info['planNum'] else None
            item['cost'] = yzy.show_str(info['cost']) if info['cost'] else None
            item['province_id'] = province_id
            item['learnYear'] = yzy.show_number(info['learnYear']) if info['learnYear'] else None
            yield item
