"""
@version:1.0
@author: endaqa
@file yzy_major_scoreline_spider.py
@time 2020/3/4 17:56
"""
import scrapy
from junyang_spider.items import YzyMajorScoreLineItem
import pymysql
from junyang_spider import settings
import json
from junyang_spider.libs import execute_js, yzy
from junyang_spider.libs.db_connection import DBConnection


class YzyMajorScoreSpider(scrapy.Spider):
    name = "yzy_major_score_line"
    allowed_domains = ["youzy.cn"]
    base_url = "https://ia-pv4y.youzy.cn"
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyMajorScorelinePipline': 100},

    }

    def start_requests(self):
        db_connect = DBConnection()
        colleges = db_connect.get_yzy_colleges()
        provinces = db_connect.get_yzy_provinces()
        db_connect.tear_down()
        # provinces = self.get_yzy_provinces()
        # print(colleges)
        # province_list = [839, 849]
        url = self.base_url + "/Data/youzy.data.scorelines.fractions.profession.query"
        year = 2020
        batch_list = [1, 2, 3, 4]
        course_list = [0, 1]
        for province in provinces:
            # url = self.base_url + "/Data/ScoreLines/Plans/Professions/Query"
            province_id = province['ProvinceId']
            for college in colleges:
                college_id = college['yzy_college_id']
                for batch_id in batch_list:
                    for course_id in course_list:
                        data_dict = {
                            'batch': str(batch_id),
                            'year': str(year),
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

    def parse(self, response):
        # 学校列表
        # print(response.text)
        province_id = response.meta['province_id']
        year = response.meta['year']
        batch_id = response.meta['batch_id']
        course_id = response.meta['course_id']
        ucodes = json.loads(response.text)['result']['uCodes']
        if ucodes:
            for ucode_dict in ucodes:
                college_enroll_code = ucode_dict['collegeCode']
                ucode = ucode_dict['uCode']
                fractions = ucode_dict['fractions']
                for info in fractions:
                    item = YzyMajorScoreLineItem()
                    item['year'] = info['year']
                    # 只要2016及以后的数据
                    minScore = info['minScore']
                    if minScore:
                        minScore = yzy.show_str(minScore)
                    avgScore = info['avgScore']
                    if avgScore:
                        avgScore = yzy.show_str(avgScore)
                    maxScore = info['maxScore']
                    if maxScore:
                        maxScore = yzy.show_str(maxScore)
                    lowSort = info['lowSort']
                    if lowSort:
                        lowSort = yzy.show_str(lowSort)
                    maxSort = info['maxSort']
                    # if maxSort and isinstance(maxSort, str):
                    #     # print(maxSort)
                    #     maxSort = yzy.show_number(maxSort)
                    enterNum = info['enterNum']
                    if enterNum:
                        enterNum = yzy.show_str(enterNum)
                    item['course'] = course_id
                    item['batch'] = info['batch']
                    item['batchName'] = info['batchName']
                    item['uCode'] = ucode
                    item['chooseLevel'] = info['chooseLevel']
                    item['lineDiff'] = None
                    item['majorCode'] = info['majorCode']
                    item['professionName'] = yzy.show_str(info['professionName']) if info['professionName'] else None
                    item['professionCode'] = None
                    item['remarks'] = None
                    item['minScore'] = minScore
                    item['avgScore'] = avgScore
                    item['maxScore'] = maxScore
                    item['lowSort'] = lowSort
                    item['maxSort'] = maxSort
                    item['enterNum'] = enterNum
                    item['countOfZJZY'] = None
                    item['province_id'] = province_id
                    item['year'] = year
                    yield item
