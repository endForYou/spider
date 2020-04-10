"""
@version:1.0
@author: endaqa
@file yzy_college_detail_spider.py
@time 2020/3/3 14:56
"""
import scrapy
from junyang_spider.items import YzyCollegeDetailItem
import pymysql
from junyang_spider import settings
import json


class YzyCollegeSpider(scrapy.Spider):
    name = "yzy_college_detail"
    allowed_domains = ["youzy.cn"]
    base_url = "https://ia-pv4y.youzy.cn"
    custom_settings = {
        'ITEM_PIPELINES': {'junyang_spider.pipelines.YzyCollegeDetailPipline': 100},

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
        sql = "select college_id from college_yzy"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def start_requests(self):
        colleges = self.get_colleges_from_db()
        # print(colleges)
        for college in colleges:
            college_id = college['college_id']
            url = self.base_url + "/Data/Colleges/Get?collegeId=%s" % college_id
            yield scrapy.Request(url, meta={'yzy_college_id': college_id}, method="POST")

    def parse(self, response):
        # 学校列表
        infos = json.loads(response.text)['result']
        meta = response.meta
        item = YzyCollegeDetailItem()
        item['college_detail_id'] = infos['id']
        print(item['college_detail_id'])
        item['yzy_college_id'] = meta['yzy_college_id']
        item['isGraduate'] = infos['isGraduate']
        item['isSport'] = infos['isSport']
        item['isRecommendedStudent'] = infos['isRecommendedStudent']
        item['isNationalDefenceStudent'] = infos['isNationalDefenceStudent']
        item['isIndependentRecruitment'] = infos['isIndependentRecruitment']
        item['tags'] = infos['tags']
        item['bxType'] = infos['bxType']
        item['star'] = infos['star']
        item['vrUrl'] = infos['vrUrl']
        item['bannerUrl'] = infos['bannerUrl']
        item['webSite'] = infos['webSite']
        item['admissionsWebSite'] = infos['admissionsWebSite']
        item['admissionsEmail'] = infos['admissionsEmail']
        item['address'] = infos['address']
        item['phone'] = infos['phone']
        item['postCode'] = infos['postCode']
        item['importClassic'] = infos['importClassic']
        item['department'] = infos['department']
        item['faculty'] = infos['faculty']
        item['addressCoordFromBaidu'] = infos['addressCoordFromBaidu']
        item['numberOfStudents'] = infos['numberOfStudents']
        item['numberOfBen'] = infos['numberOfBen']
        item['numberOfYan'] = infos['numberOfYan']
        item['numberOfBo'] = infos['numberOfBo']
        item['numberOfCJXZ'] = infos['numberOfCJXZ']
        item['numberOfYuan'] = infos['numberOfYuan']
        item['pointsOfBSH'] = infos['pointsOfBSH']
        item['countOfFollow'] = infos['countOfFollow']
        item['countOfFill'] = infos['countOfFill']
        item['countOfAP'] = infos['countOfAP']
        item['introduction'] = infos['introduction']
        item['keyMajors'] = infos['keyMajors']
        item['collegeDepartments'] = infos['collegeDepartments']
        item['numId'] = infos['numId']
        item['code'] = infos['code']
        item['logoId'] = infos['logoId']
        item['logoUrl'] = infos['logoUrl']
        item['provinceId'] = infos['provinceId']
        item['cityId'] = infos['cityId']
        item['provinceName'] = infos['provinceName']
        item['cityName'] = infos['cityName']
        item['rankOfCn'] = infos['rankOfCn']
        item['cnName'] = infos['cnName']
        item['enName'] = infos['enName']
        item['femaleRate'] = infos['femaleRate']
        item['maleRate'] = infos['maleRate']
        item['shortName'] = infos['shortName']
        item['nameUsedBefore'] = infos['nameUsedBefore']
        item['creation'] = infos['creation']
        item['educationId'] = infos['educationId']
        item['typeId'] = infos['typeId']
        item['level'] = infos['level']
        item['nature'] = infos['nature']
        item['classify'] = infos['classify']
        item['belong'] = infos['belong']
        item['belongFull'] = infos['belongFull']
        item['isArt'] = infos['isArt']
        item['isSingleRecruit'] = infos['isSingleRecruit']
        item['bxcc'] = infos['bxcc']
        item['is985'] = infos['is985']
        item['is211'] = infos['is211']
        item['isKey'] = infos['isKey']
        item['isProvincial'] = infos['isProvincial']
        item['isBTProvince'] = infos['isBTProvince']
        item['isDependent'] = infos['isDependent']
        item['isCivilianRun'] = infos['isCivilianRun']
        item['isGZDZ'] = infos['isGZDZ']
        item['hits'] = infos['hits']
        item['collegeRule'] = infos['collegeRule']
        item['majorRule'] = infos['majorRule']
        item['firstClass'] = infos['firstClass']
        item['year'] = infos['year']
        item['line'] = infos['line']
        item['plan'] = infos['plan']
        item['rankOfWorld'] = infos['rankOfWorld']
        item['rankSummary'] = infos['rankSummary']
        item['pointsOfShuo'] = infos['pointsOfShuo']
        item['pointsOfBo'] = infos['pointsOfBo']
        item['type'] = infos['type']
        item['education'] = infos['education']
        item['formatHits'] = infos['formatHits']
        item['summary'] = infos['summary']
        item['employmentRate'] = infos['employmentRate']
        item['keyMajorNum'] = infos['keyMajorNum']
        item['departmentNum'] = infos['departmentNum']
        item['keySubjectQTY'] = infos['keySubjectQTY']
        yield item
