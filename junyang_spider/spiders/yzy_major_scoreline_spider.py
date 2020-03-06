"""
@version:1.0
@author: endaqa
@file yzy_major_scoreline_spider.py
@time 2020/3/4 17:56
"""
import scrapy
from junyang_spider.items import YzyCollegeScorelineItem
import pymysql
from junyang_spider import settings
import json
from junyang_spider.libs import execute_js, yzy


class YzyMajorScoreSpider(scrapy.Spider):
    name = "yzy_major_score_line"
    allowed_domains = ["youzy.cn"]
    base_url = "https://ia-pv4y.youzy.cn"
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyMajorScorelinePipline': 100},

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
        sql = "select provinceId,uCodeNum from yzy_college_enroll_code"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        connect.close()
        return result

    def start_requests(self):
        college_enroll_codes = self.get_colleges_enroll_code_from_db()
        # print(colleges)
        for college_enroll_code in college_enroll_codes:
            province_id = college_enroll_code['ProvinceId']
            ucode = college_enroll_code['uCodeNum']
            url = self.base_url + "/Data/ScoreLines/Fractions/Professions/Query"
            data = {
                'uCode': "43_838_0_0", 'batch': 0, 'courseType': 0, 'yearFrom': 2018, 'yearTo': 2018
            }
            encrypted_hex = execute_js.encrypt_data(data)
            data = {
                'data': encrypted_hex
            }
            # print(data, college_id, province_id)
            data = {
                'province_id': province_id
            }
            yield scrapy.FormRequest(url, meta=data, method="POST", formdata=data)

    def parse(self, response):
        # 学校列表
        # print(response.text)
        province_id = response.meta['province_id']
        infos = json.loads(response.text)['result']
        for info in infos:
            # meta = response.meta
            item = YzyCollegeScorelineItem()
            item['year'] = info['year']
            # 只要2016及以后的数据
            if item['year'] < 2016:
                continue
            minScore = info['minScore']
            if minScore:
                minScore = yzy.show_number(minScore)
            avgScore = info['avgScore']
            if avgScore:
                avgScore = yzy.show_number(avgScore)
            maxScore = info['maxScore']
            if maxScore:
                maxScore = yzy.show_number(maxScore)
            lowSort = info['lowSort']
            if lowSort:
                lowSort = yzy.show_number(lowSort)
            maxSort = info['maxSort']
            if maxSort:
                maxSort = yzy.show_number(maxSort)
            enterNum = info['enterNum']
            if enterNum:
                enterNum = yzy.show_number(enterNum)
            item['course'] = info['course']
            item['batch'] = info['batch']
            item['batchName'] = info['batchName']
            item['uCode'] = info['uCode']
            item['chooseLevel'] = info['chooseLevel']
            item['lineDiff'] = info['lineDiff']
            item['minScore'] = minScore
            item['avgScore'] = avgScore
            item['maxScore'] = maxScore
            item['lowSort'] = lowSort
            item['maxSort'] = maxSort
            item['enterNum'] = enterNum
            item['countOfZJZY'] = info['countOfZJZY']
            item['prvControlLines'] = info['prvControlLines']
            item['province_id'] = province_id
            yield item
