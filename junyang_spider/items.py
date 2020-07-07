# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.pipelines.files import FilesPipeline


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


class PaperEWTItem(scrapy.Item):
    data_category = scrapy.Field()
    data_type = scrapy.Field()
    version = scrapy.Field()
    subject = scrapy.Field()
    grade = scrapy.Field()
    upload_time = scrapy.Field()
    file_url = scrapy.Field()


# class PaperEWTItem(scrapy.Item):
#     data_category = scrapy.Field()
#     data_type = scrapy.Field()
#     version = scrapy.Field()
#     subject = scrapy.Field()
#     grade = scrapy.Field()
#     upload_time = scrapy.Field()
#     file_url = scrapy.Field()


class FileDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


class NcdaItem(scrapy.Item):
    content = scrapy.Field()
    public_date = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()


class YzyCollegeItem(scrapy.Item):
    # define the fields for your item here like:
    college_name = scrapy.Field()
    college_id = scrapy.Field()
    creation_time = scrapy.Field()
    is_public = scrapy.Field()
    school_type = scrapy.Field()
    belong_to = scrapy.Field()
    is_undergraduate = scrapy.Field()
    address = scrapy.Field()
    master_station_count = scrapy.Field()
    doctor_station_count = scrapy.Field()
    school_desc = scrapy.Field()
    college_level = scrapy.Field()
    province = scrapy.Field()
    sid = scrapy.Field()


class YzyCollegeDetailItem(scrapy.Item):
    college_detail_id = scrapy.Field()
    yzy_college_id = scrapy.Field()
    isGraduate = scrapy.Field()
    isSport = scrapy.Field()
    isRecommendedStudent = scrapy.Field()
    isNationalDefenceStudent = scrapy.Field()
    isIndependentRecruitment = scrapy.Field()
    tags = scrapy.Field()
    bxType = scrapy.Field()
    star = scrapy.Field()
    vrUrl = scrapy.Field()
    bannerUrl = scrapy.Field()
    webSite = scrapy.Field()
    admissionsWebSite = scrapy.Field()
    admissionsEmail = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    postCode = scrapy.Field()
    importClassic = scrapy.Field()
    department = scrapy.Field()
    faculty = scrapy.Field()
    addressCoordFromBaidu = scrapy.Field()
    numberOfStudents = scrapy.Field()
    numberOfBen = scrapy.Field()
    numberOfYan = scrapy.Field()
    numberOfBo = scrapy.Field()
    numberOfCJXZ = scrapy.Field()
    numberOfYuan = scrapy.Field()
    pointsOfBSH = scrapy.Field()
    countOfFollow = scrapy.Field()
    countOfFill = scrapy.Field()
    countOfAP = scrapy.Field()
    introduction = scrapy.Field()
    keyMajors = scrapy.Field()
    collegeDepartments = scrapy.Field()
    numId = scrapy.Field()
    code = scrapy.Field()
    logoId = scrapy.Field()
    logoUrl = scrapy.Field()
    provinceId = scrapy.Field()
    cityId = scrapy.Field()
    provinceName = scrapy.Field()
    cityName = scrapy.Field()
    rankOfCn = scrapy.Field()
    cnName = scrapy.Field()
    enName = scrapy.Field()
    femaleRate = scrapy.Field()
    maleRate = scrapy.Field()
    shortName = scrapy.Field()
    nameUsedBefore = scrapy.Field()
    creation = scrapy.Field()
    educationId = scrapy.Field()
    typeId = scrapy.Field()
    level = scrapy.Field()
    nature = scrapy.Field()
    classify = scrapy.Field()
    belong = scrapy.Field()
    belongFull = scrapy.Field()
    isArt = scrapy.Field()
    isSingleRecruit = scrapy.Field()
    bxcc = scrapy.Field()
    is985 = scrapy.Field()
    is211 = scrapy.Field()
    isKey = scrapy.Field()
    isProvincial = scrapy.Field()
    isBTProvince = scrapy.Field()
    isDependent = scrapy.Field()
    isCivilianRun = scrapy.Field()
    isGZDZ = scrapy.Field()
    hits = scrapy.Field()
    collegeRule = scrapy.Field()
    majorRule = scrapy.Field()
    firstClass = scrapy.Field()
    year = scrapy.Field()
    line = scrapy.Field()
    plan = scrapy.Field()
    rankOfWorld = scrapy.Field()
    rankSummary = scrapy.Field()
    pointsOfShuo = scrapy.Field()
    pointsOfBo = scrapy.Field()
    type = scrapy.Field()
    education = scrapy.Field()
    formatHits = scrapy.Field()
    summary = scrapy.Field()
    employmentRate = scrapy.Field()
    keyMajorNum = scrapy.Field()
    departmentNum = scrapy.Field()
    keySubjectQTY = scrapy.Field()


class YzyCollegeEnrollCodeItem(scrapy.Item):
    provinceId = scrapy.Field()
    provinceName = scrapy.Field()
    uCodeNum = scrapy.Field()
    admissCode = scrapy.Field()
    collegeId = scrapy.Field()
    collegeName = scrapy.Field()
    sort = scrapy.Field()
    isOld = scrapy.Field()
    codeChangeYear = scrapy.Field()
    str_id = scrapy.Field()


class YzyCollegeScorelineItem(scrapy.Item):
    year = scrapy.Field()
    course = scrapy.Field()
    batch = scrapy.Field()
    batchName = scrapy.Field()
    uCode = scrapy.Field()
    chooseLevel = scrapy.Field()
    lineDiff = scrapy.Field()
    minScore = scrapy.Field()
    avgScore = scrapy.Field()
    maxScore = scrapy.Field()
    lowSort = scrapy.Field()
    maxSort = scrapy.Field()
    enterNum = scrapy.Field()
    countOfZJZY = scrapy.Field()
    prvControlLines = scrapy.Field()
    province_id = scrapy.Field()


class YzyMajorScoreLineItem(scrapy.Item):
    year = scrapy.Field()
    course = scrapy.Field()
    batch = scrapy.Field()
    batchName = scrapy.Field()
    uCode = scrapy.Field()
    chooseLevel = scrapy.Field()
    lineDiff = scrapy.Field()
    majorCode = scrapy.Field()
    professionName = scrapy.Field()
    professionCode = scrapy.Field()
    remarks = scrapy.Field()
    minScore = scrapy.Field()
    avgScore = scrapy.Field()
    maxScore = scrapy.Field()
    lowSort = scrapy.Field()
    maxSort = scrapy.Field()
    enterNum = scrapy.Field()
    countOfZJZY = scrapy.Field()
    province_id = scrapy.Field()


class YzyMajorItem(scrapy.Item):
    category_name = scrapy.Field()
    category_code = scrapy.Field()
    subcategory_name = scrapy.Field()
    subcategory_code = scrapy.Field()
    major_name = scrapy.Field()
    major_code = scrapy.Field()
    grade = scrapy.Field()


class YzyMajorDetailItem(scrapy.Item):
    major_name = scrapy.Field()
    major_code = scrapy.Field()
    grade = scrapy.Field()
    courses = scrapy.Field()
    description = scrapy.Field()
    employment = scrapy.Field()
    inherit_secondary_vocational = scrapy.Field()
    inherit_undergraduate = scrapy.Field()
    job_qualification_certificate = scrapy.Field()
    knowledge = scrapy.Field()
    schooling_time = scrapy.Field()
    degree = scrapy.Field()


class YzyEnrollPlanItem(scrapy.Item):
    year = scrapy.Field()
    courseType = scrapy.Field()
    batch = scrapy.Field()
    batchName = scrapy.Field()
    uCode = scrapy.Field()
    majorCode = scrapy.Field()
    professionName = scrapy.Field()
    professionCode = scrapy.Field()
    planNum = scrapy.Field()
    cost = scrapy.Field()
    learnYear = scrapy.Field()
    province_id = scrapy.Field()


class YzyEnrollGuideItem(scrapy.Item):
    content = scrapy.Field()
    publish_date = scrapy.Field()
    title = scrapy.Field()
    college_id = scrapy.Field()


class YzyCollegeMajorItem(scrapy.Item):
    college_id = scrapy.Field()
    college_name = scrapy.Field()
    major_name = scrapy.Field()
    yzy_college_id = scrapy.Field()
    grade = scrapy.Field()
