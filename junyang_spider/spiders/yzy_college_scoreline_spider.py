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


class YzyCollegeScorelineSpider(scrapy.Spider):
    name = "yzy_college_scoreline"
    allowed_domains = ["youzy.cn"]
    base_url = "https://ia-pv4y.youzy.cn"
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyCollegeScorelinePipline': 100},

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
        # sql = "select provinceId,uCodeNum from yzy_college_enroll_code where provinceId in (select ProvinceId from yzy_province where Used=1)"
        sql = "select provinceId,uCodeNum from yzy_college_enroll_code where provinceId=850"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        connect.close()
        return result

    def get_colleges(self):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        sql = "select DISTINCT yzy_college_id from yzy_college"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        connect.close()
        return result

    def get_yzy_provinces(self):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        sql = "select ProvinceId  from yzy_province where Used=1"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        connect.close()
        return result

    def start_requests(self):
        # college_enroll_codes = self.get_colleges_enroll_code_from_db()
        colleges = self.get_colleges()
        provinces = self.get_yzy_provinces()
        # print(colleges)
        for college in colleges:
            for province in provinces:
                province_id = province['ProvinceId']
                college_id = college['yzy_college_id']
                # college_id = '838'
                # url = self.base_url + "/Data/ScoreLines/Fractions/Colleges/Query"
                url = self.base_url + "/Data/youzy.data.scorelines.fractions.college.query"
                data = {
                    'provinceId': province_id,
                    'collegeId': college_id,
                    'courseId': 0
                }
                # print(ucode)
                encrypted_hex = execute_js.encrypt_data(data)
                data = {
                    'data': encrypted_hex
                }
                print(data)
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
                # yield scrapy.Request(url, method="POST", body=json.dumps(data), headers=headers)
                yield scrapy.FormRequest(url, meta=meta, method="POST", formdata=data)

    def parse(self, response):
        res = json.loads(response.text)
        print(res, 111111111111)
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
                    if minScore:
                        # print(minScore)
                        minScore = yzy.show_number(minScore)
                    avgScore = info['avgScore']
                    if avgScore:
                        # print(avgScore)
                        avgScore = yzy.show_number(avgScore)
                    maxScore = info['maxScore']
                    if maxScore:
                        # print(maxScore)
                        maxScore = yzy.show_number(maxScore)
                    lowSort = info['lowSort']
                    if lowSort:
                        # print(lowSort)
                        lowSort = yzy.show_number(lowSort)
                    maxSort = info['maxSort']
                    if maxSort and isinstance(maxSort, str):
                        # print(maxSort)
                        maxSort = yzy.show_number(maxSort)
                    enterNum = info['enterNum']
                    if enterNum:
                        # print(enterNum)
                        enterNum = yzy.show_number(enterNum)

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
