"""
@version:1.0
@author: endaqa
@file yzy_major_scoreline_spider.py
@time 2020/3/4 17:56
"""
import scrapy
from junyang_spider.items import YzyEnrollPlanItem
from junyang_spider.libs.db_connection import DBConnection
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

    def start_requests(self):
        db_connect = DBConnection()
        colleges = db_connect.get_yzy_colleges()
        db_connect.tear_down()
        # provinces = self.get_yzy_provinces()
        # print(colleges)
        province_list = [849, ]
        for province_id in province_list:
            # url = self.base_url + "/Data/ScoreLines/Plans/Professions/Query"
            url = self.base_url + "/Data/youzy.data.scorelines.plan.query"
            year = 2020
            # 按不同的省份设置
            batch_list = [1, 2, 3]
            course_list = [0, 1]
            for college in colleges:
                college_id = college['yzy_college_id']
                for batch_id in batch_list:
                    for course_id in course_list:
                        data_dict = {
                            'batch': batch_id,
                            'year': year,
                            'provinceId': province_id,
                            'collegeId': str(college_id),
                            'courseId': course_id
                        }

                        encrypted_hex = execute_js.encrypt_data(data_dict)
                        # print(encrypted_hex)
                        data = {
                            'data': encrypted_hex
                        }
                        # print(data_dict)
                        # print(data)
                        # print(data, college_id, province_id)
                        meta_data = {
                            'province_id': province_id,
                            'year': year,
                            'course_id': course_id,
                            'batch_id': batch_id
                        }
                        yield scrapy.Request(url, meta=meta_data, method="POST", body=json.dumps(data))
                        # yield scrapy.FormRequest(url, meta=meta_data, method="POST", formdata=data)

    def parse(self, response):
        # 招生计划列表
        # print(response.text)
        # print(response.text)
        province_id = response.meta['province_id']
        year = response.meta['year']
        batch_id = response.meta['batch_id']
        course_id = response.meta['course_id']
        if response.text:
            print(response.text, 1111)
            ucodes = json.loads(response.text)['result']['uCodes']
            if ucodes:
                for ucode_dict in ucodes:
                    college_enroll_code = ucode_dict['collegeCode']
                    ucode = ucode_dict['uCode']
                    fractions = ucode_dict['fractions']
                    for fraction in fractions[1:]:
                        data_type = fraction['dataType']
                        # print(data_type)
                        item = YzyEnrollPlanItem()
                        item['courseType'] = course_id
                        item['batch'] = batch_id
                        item['uCode'] = ucode
                        item['year'] = year
                        item['province_id'] = province_id

                        item['batchName'] = fractions[0]['batchName']
                        # item['batchName'] = None  # 先初始化
                        # if data_type == 1:
                        #     print(1111111111111)
                        # else:
                        # if data_type == 2:
                        # meta = response.meta

                        # 只要2016及以后的数据
                        item['majorCode'] = fraction['majorCode']
                        item['professionName'] = yzy.show_str(fraction['name']) if fraction[
                            'name'] else None
                        item['professionCode'] = yzy.show_str(fraction['code']) if fraction[
                            'code'] else None
                        item['planNum'] = yzy.show_str(fraction['planNum']) if fraction['planNum'] else None
                        item['cost'] = yzy.show_str(fraction['cost']) if fraction['cost'] else None

                        item['learnYear'] = yzy.show_str(fraction['learnYear']) if fraction['learnYear'] else None
                        yield item
