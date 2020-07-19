"""
@version:1.0
@author: endaqa
@file yzy_college_scoreline_spider.py
@time 2020/3/4 15:15
"""

import scrapy
from junyang_spider.items import YzyCollegeScorelineItem
import pymysql
from junyang_spider import settings
import json
from junyang_spider.libs import execute_js, yzy
from junyang_spider.libs.db_connection import DBConnection


class YzyCollegeScorelineSpider(scrapy.Spider):
    name = "yzy_college_scoreline"
    allowed_domains = ["youzy.cn"]
    base_url = "https://ia-pv4y.youzy.cn"
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyCollegeScorelinePipline': 100},

    }

    def start_requests(self):
        db_connect = DBConnection()
        colleges = db_connect.get_yzy_colleges()
        provinces = db_connect.get_yzy_provinces()
        db_connect.tear_down()
        # print(colleges)
        for college in colleges:
            college_id = college['yzy_college_id']
            for province in provinces:
                province_id = province['ProvinceId']
                #print(college_id, province_id)
                # college_id = '838'
                # url = self.base_url + "/Data/ScoreLines/Fractions/Colleges/Query"
                url = self.base_url + "/Data/youzy.data.scorelines.fractions.college.query"
                data = {
                    'provinceId': province_id,
                    'collegeId': str(college_id),
                    'courseId': 0
                }
                # print(ucode)
                encrypted_hex = execute_js.encrypt_data(data)
                data = {
                    'data': encrypted_hex
                }
                #print(data)
                # print(province_id, ucode,encrypted_hex)
                # print(data, college_id, province_id)
                meta = {
                    'province_id': province_id
                }
                # headers = {
                #     'Cookie': 'UM_distinctid=172e602865d127-02ab4bbbae8b5f-4353761-1fa400-172e602865e3d1; connect.sid=s%3AIA4ohb_eUeZw8CvONFcdOOYdkg0zfTKl.in2vgkY465gWSzIOkJG1NMczaeGd8VJYq4FxxaGKHRg; youzy.pv4y.type=toC; youzy.pv4y.uid=e559340d34eb5c56',
                #     'Content-Type': 'application/json',
                #     'Accept': 'application/json, text/javascript, */*; q=0.01',
                #     'Origin': 'https://ia-pv4y.youzy.cn'
                #
                # }
                yield scrapy.Request(url, method="POST", meta=meta, body=json.dumps(data))
                # yield scrapy.FormRequest(url, meta=meta, method="POST", formdata=data)

    def parse(self, response):
        res = json.loads(response.text)
        # print(res, 111111111111)
        province_id = response.meta['province_id']
        if res:
            courses = res['result'][0]['courses']
            for data in courses:
                fractions = data['fractions']
                for info in fractions:
                    # meta = response.meta
                    item = YzyCollegeScorelineItem()
                    item['year'] = info['year']
                    # 只要2016及以后的数据
                    if item['year'] < 2016:
                        continue
                    minScore = info['minScore']
                    if minScore and minScore != "0":
                        # print(minScore)
                        minScore = yzy.show_str(minScore)
                    avgScore = info['avgScore']
                    if avgScore and avgScore != "0":
                        # print(avgScore)
                        avgScore = yzy.show_str(avgScore)
                    maxScore = info['maxScore']
                    if maxScore and maxScore != "0":
                        # print(maxScore)
                        maxScore = yzy.show_str(maxScore)
                    lowSort = info['lowSort']
                    if lowSort and lowSort != "0":
                        # print(lowSort)
                        lowSort = yzy.show_str(lowSort)
                    maxSort = info['maxSort']
                    # if maxSort and maxSort != "0" and isinstance(maxSort, str):
                    #     # print(maxSort)
                    #     print(maxSort,111111)
                    #     maxSort = yzy.show_str(maxSort)
                    enterNum = info['enterNum']
                    if enterNum and enterNum != "0":
                        # print(enterNum)
                        enterNum = yzy.show_str(enterNum)

                    item['course'] = info['course']
                    item['batch'] = info['batch']
                    item['batchName'] = info['batchName']
                    item['uCode'] = info['uCode']
                    item['chooseLevel'] = info['chooseLevel']
                    item['lineDiff'] = None
                    item['minScore'] = minScore
                    item['avgScore'] = avgScore
                    item['maxScore'] = maxScore
                    item['lowSort'] = lowSort
                    item['maxSort'] = maxSort
                    item['enterNum'] = enterNum
                    item['province_id'] = province_id
                    yield item

    # def parse(self, response):
    #     result = json.loads(response.text)
    #     # print(result)
    #     if result:
    #
    #         province_id = response.meta['province_id']
    #         infos = result['result']
    #         for info in infos:
    #             # meta = response.meta
    #             item = YzyCollegeScorelineItem()
    #             item['year'] = info['year']
    #             # 只要2016及以后的数据
    #             if item['year'] < 2016:
    #                 continue
    #             minScore = info['minScore']
    #             if minScore:
    #                 # print(minScore)
    #                 minScore = yzy.show_number(minScore)
    #             avgScore = info['avgScore']
    #             if avgScore:
    #                 # print(avgScore)
    #                 avgScore = yzy.show_number(avgScore)
    #             maxScore = info['maxScore']
    #             if maxScore:
    #                 # print(maxScore)
    #                 maxScore = yzy.show_number(maxScore)
    #             lowSort = info['lowSort']
    #             if lowSort:
    #                 # print(lowSort)
    #                 lowSort = yzy.show_number(lowSort)
    #             maxSort = info['maxSort']
    #             if maxSort and isinstance(maxSort, str):
    #                 # print(maxSort)
    #                 maxSort = yzy.show_number(maxSort)
    #             enterNum = info['enterNum']
    #             if enterNum:
    #                 # print(enterNum)
    #                 enterNum = yzy.show_number(enterNum)
    #
    #             item['course'] = info['course']
    #             item['batch'] = info['batch']
    #             item['batchName'] = info['batchName']
    #             item['uCode'] = info['uCode']
    #             item['chooseLevel'] = info['chooseLevel']
    #             item['lineDiff'] = info['lineDiff']
    #             item['minScore'] = minScore
    #             item['avgScore'] = avgScore
    #             item['maxScore'] = maxScore
    #             item['lowSort'] = lowSort
    #             item['maxSort'] = maxSort
    #             item['enterNum'] = enterNum
    #             item['countOfZJZY'] = info['countOfZJZY']
    #             item['prvControlLines'] = info['prvControlLines']
    #             item['province_id'] = province_id
    #             yield item
