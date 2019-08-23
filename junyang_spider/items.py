# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JunyangSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FoJobItem(scrapy.Item):
    Id = scrapy.Field()  # JobId
    Rid = scrapy.Field()
    Fid = scrapy.Field()
    FuncDepart = scrapy.Field()  # 职能部门
    JobUrl = scrapy.Field()  # 招聘所在url
    JobTitle = scrapy.Field()  # 标题
    CompanyName = scrapy.Field()  # 公司名
    CompanyLocation = scrapy.Field()  # 公司坐标
    CompanyType = scrapy.Field()  # 公司类型
    CompanyPeople = scrapy.Field()  # 公司工作人数
    CompanyAddress = scrapy.Field()  # 公司地址
    CompanyProfile = scrapy.Field()  # 公司简介
    CompanyIndustry = scrapy.Field()  # 公司行业
    CompanyDepart = scrapy.Field()  # 部门信息
    CompanyBenefits = scrapy.Field()  # 公司福利
    RequireInfo = scrapy.Field()  # 发布日期
    SalaryRange = scrapy.Field()  # 薪资待遇范围

    JobInfo = scrapy.Field()  # 职位信息
    Functions = scrapy.Field()  # 职能类别
    KeyWords = scrapy.Field()  # 关键字


# def __str__(self):
# 	"""only print out attr1 after exiting the Pipeline"""
# 	return ""


class RegionItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()


class GkItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    name_of_major = scrapy.Field()
    subject = scrapy.Field()
    type = scrapy.Field()
    major_code = scrapy.Field()
    career_can_be = scrapy.Field()
    major_desc = scrapy.Field()
    similar_major = scrapy.Field()


class GkqItem(scrapy.Item):
    # define the fields for your item here like:
    more_bigger_type = scrapy.Field()
    major_type = scrapy.Field()
    profession = scrapy.Field()
    job_prospect = scrapy.Field()


class YGGKItem(scrapy.Item):
    # define the fields for your item here like:
    school_name = scrapy.Field()  # 学校名字
    school_location = scrapy.Field()
    school_type = scrapy.Field()
    education_level = scrapy.Field()
    school_feature = scrapy.Field()
    school_desc = scrapy.Field()
    school_url = scrapy.Field()
    school_address = scrapy.Field()
    major_desc = scrapy.Field()
    scholarship = scrapy.Field()
    food_and_stay_condition = scrapy.Field()
    student_employment = scrapy.Field()
    infrastructure = scrapy.Field()


class YGGKZhaoShengItem(scrapy.Item):
    # define the fields for your item here like:
    school_name = scrapy.Field()  # 学校名字
    enrollment_guide_of_2018 = scrapy.Field()
    enrollment_guide_of_2017 = scrapy.Field()


class EolEntryScoreItem(scrapy.Item):
    # define the fields for your item here like:
    school_name = scrapy.Field()  # 学校名字
    major_name = scrapy.Field()
    enroll_place = scrapy.Field()
    major_type = scrapy.Field()
    years = scrapy.Field()
    enroll_batch = scrapy.Field()
    average_score = scrapy.Field()


class MajorRankItem(scrapy.Item):
    PKid = scrapy.Field()
    school_name = scrapy.Field()
    school_code = scrapy.Field()
    major_type = scrapy.Field()
    major_code = scrapy.Field()
    major_big_type = scrapy.Field()
    major_rank = scrapy.Field()


class GkqSchoolItem(scrapy.Item):
    # define the fields for your item here like:
    school_name = scrapy.Field()
    creation_time = scrapy.Field()
    key_subject_count = scrapy.Field()
    students_count = scrapy.Field()
    academician_count = scrapy.Field()
    doctor_station_count = scrapy.Field()
    master_station_count = scrapy.Field()
    school_desc = scrapy.Field()
    national_key_discipline = scrapy.Field()
    feature_specialty = scrapy.Field()
    top_discipline = scrapy.Field()
    national_key_laboratory = scrapy.Field()
    self_enrollment = scrapy.Field()


class MiddleSchoolItem(scrapy.Item):
    school_name = scrapy.Field()
    location = scrapy.Field()
    school_nature = scrapy.Field()
    school_level = scrapy.Field()
    phone = scrapy.Field()
    school_type = scrapy.Field()
    school_mail = scrapy.Field()
    school_url = scrapy.Field()
    class_nums = scrapy.Field()
    school_address = scrapy.Field()
    postcode = scrapy.Field()
    school_desc = scrapy.Field()


class EOLEntryScoreItem(scrapy.Item):
    # define the fields for your item here like:
    province = scrapy.Field()
    major_type = scrapy.Field()
    years = scrapy.Field()
    batch = scrapy.Field()
    rank_line = scrapy.Field()


class GkcxCollegeEntryScoreItem(scrapy.Item):
    # define the fields for your item here like:
    school_name = scrapy.Field()  # 学校名字
    enroll_place = scrapy.Field()
    province = scrapy.Field()
    major_type = scrapy.Field()
    years = scrapy.Field()
    enroll_batch = scrapy.Field()
    average_score = scrapy.Field()
    province_line = scrapy.Field()
    line_difference = scrapy.Field()
    min = scrapy.Field()


class SchoolRankItem(scrapy.Item):
    PKid = scrapy.Field()
    school_name = scrapy.Field()
    school_rank = scrapy.Field()
    major_type = scrapy.Field()
    major_code = scrapy.Field()
    major_big_type = scrapy.Field()
    major_rank = scrapy.Field()


class ScoreDistributionItem(scrapy.Item):
    score = scrapy.Field()
    people = scrapy.Field()
    accumulative_people = scrapy.Field()
    accumulative_rate = scrapy.Field()


class YouzyItem(scrapy.Item):
    school = scrapy.Field()
    major = scrapy.Field()


class YouzySchoolBadgeItem(scrapy.Item):
    school_name = scrapy.Field()
    image_url = scrapy.Field()
    image_paths = scrapy.Field()


class KeyMajorItem(scrapy.Item):
    big_type = scrapy.Field()
    type1 = scrapy.Field()
    code = scrapy.Field()
    type2 = scrapy.Field()
    type3 = scrapy.Field()
    school = scrapy.Field()


class BaiduSchoolItem(scrapy.Item):
    province = scrapy.Field()
    school = scrapy.Field()
    precedence = scrapy.Field()
    min = scrapy.Field()
    average = scrapy.Field()
    curriculum = scrapy.Field()
    batch = scrapy.Field()
    num = scrapy.Field()
    year = scrapy.Field()
    batchscore = scrapy.Field()


class XuanKeRequirementsItem(scrapy.Item):
    area = scrapy.Field()
    school_code = scrapy.Field()
    school_name = scrapy.Field()
    url = scrapy.Field()
    level = scrapy.Field()
    major_name = scrapy.Field()
    requirements = scrapy.Field()
    major_in = scrapy.Field()


class SubjectRequirementsItem(scrapy.Item):
    province = scrapy.Field()
    college_province = scrapy.Field()
    college_name = scrapy.Field()
    grade = scrapy.Field()
    major_name = scrapy.Field()
    requirements = scrapy.Field()


class SchoolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    # 校区
    allTypesBySchool = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    year = scrapy.Field()
    province = scrapy.Field()
