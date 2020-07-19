# -*- coding: utf-8 -*-
import pymysql, pymongo, re
from twisted.internet.threads import deferToThread
from twisted.enterprise import adbapi
from pymysql.err import IntegrityError, ProgrammingError
from scrapy.exceptions import CloseSpider


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JunyangSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class SchoolPipeline(object):
    def process_item(self, item, spider):
        return item


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FoJobPipeline(object):
    def process_item(self, item, spider):
        return item


# class SchoolBadgePipeline(object):
#     def process_item(self, item, spider):
#         images = []
#         # 所有图片放在一个文件夹下
#         dir_path = '{}'.format(IMAGES_STORE)
#         if not os.path.exists(dir_path) and len(item['src']) != 0:
#             os.mkdir(dir_path)
#         for jpg_url, name, num in zip(item['src'], item['school_name'], range(0, 100)):
#             file_name = name + str(num)
#             file_path = '{}//{}'.format(dir_path, file_name)
#             images.append(file_path)
#             if os.path.exists(file_path) or os.path.exists(file_name):
#                 continue
#             with open('{}//{}.jpg'.format(dir_path, file_name), 'wb') as f:
#                 req = requests.get(jpg_url, headers=header)
#                 f.write(req.content)
#
#         return item


class RegionPipeline(object):
    regionInsert = "insert into region(name,code) values('{name}','{code}')"
    functionInsert = "insert into function(name,code) values('{name}','{code}')"
    industryInsert = "insert into industry(name,code) values('{name}','{code}')"

    def __init__(self, settings):
        self.settings = settings
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if spider.name == "areaspider":
            sqltext = self.regionInsert.format(
                name=pymysql.escape_string(item['name']),
                code=pymysql.escape_string(item['code'])
            )
            # spider.log(sqltext)
            self.cursor.execute(sqltext)
        elif spider.name == "function":
            sqltext = self.functionInsert.format(
                name=pymysql.escape_string(item['name']),
                code=pymysql.escape_string(item['code']),
            )
            # spider.log(sqltext)
            self.cursor.execute(sqltext)
        elif spider.name == "industry":
            sqltext = self.industryInsert.format(
                name=pymysql.escape_string(item['name']),
                code=pymysql.escape_string(item['code']),
            )
            # spider.log(sqltext)
            self.cursor.execute(sqltext)
        else:
            spider.log('Undefined name: %s' % spider.name)

        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        # 通过cursor执行增删查改
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


class MongoPipeline(object):
    collection_name = 'FoJobData'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def _process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)


class MysqlPipeline(MongoPipeline):
    def __init__(self, settings):
        super(MysqlPipeline, self).__init__(settings.get('MONGO_URI'), settings.get('MONGO_DATABASE'))
        self.settings = settings
        self.mongo_client = pymongo.MongoClient(self.mongo_uri)
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        if self.mongo_db[self.collection_name].count() >= self.settings.get('INSERT_LIMIT'):

            # item['JobInfo'] = pymysql.escape_string(item['JobInfo'])
            # item['CompanyProfile'] = pymysql.escape_string(item['CompanyProfile'])
            collections = self.mongo_db[self.collection_name].find({})
            iteration = list(collections)
            removelist = iteration

            for doc in iteration:
                # region = re.search('51job.com/(.*?)/',doc.get('JobUrl')).group(1).split('-')[0]
                insert = f"insert into jobinfo19823({','.join(item.keys())}) values(" + ','.join(
                    ['"{' + k + '}"' for k in item.keys()]) + ")"
                doc = {k: pymysql.escape_string(v) if isinstance(v, str) else v for k, v in doc.items()}
                sqltext = insert.format(**doc)
                self.cursor.execute(sqltext)

                # create_sql = f"CREATE TABLE IF NOT EXISTS jobinfo_{region} Like jobinfo"
                # self.cursor.execute(create_sql)

            ids_to_remove = [i.get('_id') for i in removelist]
            self.mongo_db[self.collection_name].delete_many({'_id': {'$in': ids_to_remove}})
            # self.mongo_db[self.collection_name].remove({"ResumeUrl":doc['ResumeUrl']})
            self.connect.commit()  # 提交到数据库执行
        return item

    def open_spider(self, spider):
        # 连接数据库

        # 通过cursor执行增删查改
        self.mongo_db = self.mongo_client[self.mongo_db]

    # self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


class PaperEWTPipeline:
    def process_item(self, item, spider):
        return item


class YzyCollegeDetailPipline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        # print("11111111111",item)
        # print("111111111111111111111111111111111111111111111111111111111111111111111111")
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = '''INSERT INTO yzy_college (did,yzy_college_id,isGraduate,isSport,isRecommendedStudent,isNationalDefenceStudent,
    isIndependentRecruitment,tags,bxType,star,vrUrl,bannerUrl,webSite,admissionsWebSite,admissionsEmail,address,phone,postCode,importClassic
    ,department,faculty,addressCoordFromBaidu,numberOfStudents,numberOfBen,numberOfYan,numberOfBo,numberOfCJXZ,numberOfYuan,
   pointsOfBSH,countOfFollow, countOfFill,countOfAP,introduction,keyMajors,collegeDepartments,numId,code,logoId,logoUrl,
   provinceId,cityId,provinceName,cityName,rankOfCn,cnName,enName,femaleRate,maleRate,shortName,nameUsedBefore,creation,
   educationId,typeId,level,nature,classify,belong,belongFull,isArt,isSingleRecruit,bxcc,is985,is211,isKey,isProvincial,
   isBTProvince,isDependent,isCivilianRun,isGZDZ,hits,collegeRule,majorRule,firstClass,year,line,plan,rankOfWorld,rankSummary,
   pointsOfShuo,pointsOfBo,type,education,formatHits,summary,employmentRate,keyMajorNum,departmentNum,keySubjectQTY )
     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
     ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
     ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
        # 执行sql语句
        college_detail_id = item['college_detail_id']
        yzy_college_id = item['yzy_college_id']
        isGraduate = item['isGraduate']
        isSport = item['isSport']
        isRecommendedStudent = item['isRecommendedStudent']
        isNationalDefenceStudent = item['isNationalDefenceStudent']
        isIndependentRecruitment = item['isIndependentRecruitment']
        tags = item['tags']
        bxType = item['bxType']
        star = item['star']
        vrUrl = item['vrUrl']
        bannerUrl = item['bannerUrl']
        webSite = item['admissionsWebSite']
        admissionsWebSite = item['admissionsWebSite']
        admissionsEmail = item['admissionsEmail']
        address = item['address']
        phone = item['phone']
        postCode = item['postCode']
        importClassic = item['importClassic']
        department = item['department']
        faculty = item['faculty']
        addressCoordFromBaidu = item['addressCoordFromBaidu']
        numberOfStudents = item['numberOfStudents']
        numberOfBen = item['numberOfBen']
        numberOfYan = item['numberOfYan']
        numberOfBo = item['numberOfBo']
        numberOfCJXZ = item['numberOfCJXZ']
        numberOfYuan = item['numberOfYuan']
        pointsOfBSH = item['pointsOfBSH']
        countOfFollow = item['countOfFollow']
        countOfFill = item['countOfFill']
        countOfAP = item['countOfAP']
        introduction = item['introduction']
        keyMajors = item['keyMajors']
        collegeDepartments = item['collegeDepartments']
        numId = item['numId']
        code = item['code']
        logoId = item['logoId']
        logoUrl = item['logoUrl']
        provinceId = item['provinceId']
        cityId = item['cityId']
        provinceName = item['provinceName']
        cityName = item['cityName']
        rankOfCn = item['rankOfCn']
        cnName = item['cnName']
        enName = item['enName']
        femaleRate = item['femaleRate']
        maleRate = item['maleRate']
        shortName = item['shortName']
        nameUsedBefore = item['nameUsedBefore']
        creation = item['creation']
        educationId = item['educationId']
        typeId = item['typeId']
        level = item['level']
        nature = item['nature']
        classify = item['classify']
        belong = item['belong']
        belongFull = item['belongFull']
        isArt = item['isArt']
        isSingleRecruit = item['isSingleRecruit']
        bxcc = item['bxcc']
        is985 = item['is985']
        is211 = item['is211']
        isKey = item['isKey']
        isProvincial = item['isProvincial']
        isBTProvince = item['isBTProvince']
        isDependent = item['isDependent']
        isCivilianRun = item['isCivilianRun']
        isGZDZ = item['isGZDZ']
        hits = item['hits']
        collegeRule = item['collegeRule']
        majorRule = item['majorRule']
        firstClass = item['firstClass']
        year = item['year']
        line = item['line']
        plan = item['plan']
        rankOfWorld = item['rankOfWorld']
        rankSummary = item['rankSummary']
        pointsOfShuo = item['pointsOfShuo']
        pointsOfBo = item['pointsOfBo']
        type = item['type']
        education = item['education']
        formatHits = item['formatHits']
        summary = item['summary']
        employmentRate = item['employmentRate']
        keyMajorNum = item['keyMajorNum']
        departmentNum = item['departmentNum']
        keySubjectQTY = item['keySubjectQTY']
        # print("111111111111111111111111111111111111111111111111111111111111111111111111")
        cursor.execute(sql, (
            college_detail_id, yzy_college_id, isGraduate, isSport, isRecommendedStudent, isNationalDefenceStudent,
            isIndependentRecruitment, tags, bxType, star, vrUrl, bannerUrl, webSite, admissionsWebSite,
            admissionsEmail, address, phone, postCode, importClassic
            , department, faculty, addressCoordFromBaidu, numberOfStudents, numberOfBen, numberOfYan,
            numberOfBo, numberOfCJXZ, numberOfYuan,
            pointsOfBSH, countOfFollow, countOfFill, countOfAP, introduction, keyMajors, collegeDepartments,
            numId, code, logoId, logoUrl,
            provinceId, cityId, provinceName, cityName, rankOfCn, cnName, enName, femaleRate, maleRate,
            shortName, nameUsedBefore, creation,
            educationId, typeId, level, nature, classify, belong, belongFull, isArt, isSingleRecruit, bxcc,
            is985, is211, isKey, isProvincial,
            isBTProvince, isDependent, isCivilianRun, isGZDZ, hits, collegeRule, majorRule, firstClass,
            year, line, plan, rankOfWorld, rankSummary,
            pointsOfShuo, pointsOfBo, type, education, formatHits, summary, employmentRate, keyMajorNum,
            departmentNum, keySubjectQTY))

        # 错误函数

    def handle_error(self, failure, item, spider):
        print(failure)


class YzyCollegePipeline(object):
    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = '''INSERT INTO college_yzy (is_public,college_name,creation_time,school_type,belong_to,is_undergraduate,
province,address,master_station_count,doctor_station_count,school_desc,college_id,college_level,sid)
 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''
        # 执行sql语句
        is_public = item['is_public']
        college_name = item['college_name']
        creation_time = item['creation_time']
        school_type = item['school_type']
        belong_to = item['belong_to']
        is_undergraduate = item['is_undergraduate']
        address = item['address']
        master_station_count = item['master_station_count']
        doctor_station_count = item['doctor_station_count']
        school_desc = item['school_desc']
        college_id = item['college_id']
        college_level = item['college_level']
        province = item['province']
        sid = item['sid']
        cursor.execute(sql, (is_public, college_name, creation_time, school_type, belong_to, is_undergraduate,
                             province, address, master_station_count, doctor_station_count, school_desc, college_id,
                             college_level, sid))
        # 错误函数

    def handle_error(self, failure, item, spider):
        print(failure)


class NcdaPipeline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO ncda_article (author,title,public_date,content,category) VALUES (%s,%s,%s,%s,%s)"
        # 执行sql语句
        author = item['author']
        title = item['title']
        public_date = item['public_date']
        content = item['content']
        category = item['category']
        cursor.execute(sql, (author, title, public_date, content, category))
        # 错误函数

    def handle_error(self, failure, item, spider):
        print(failure)


class YzyCollegeEnrollCodePipline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = '''INSERT INTO yzy_college_enroll_code_new (provinceId,provinceName,uCodeNum,admissCode,collegeId,collegeName
,sort,isOld,codeChangeYear,str_id)
 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''
        # 执行sql语句
        provinceId = item['provinceId']
        provinceName = item['provinceName']
        uCodeNum = item['uCodeNum']
        admissCode = item['admissCode']
        collegeId = item['collegeId']
        collegeName = item['collegeName']
        sort = item['sort']
        isOld = item['isOld']
        codeChangeYear = item['codeChangeYear']
        str_id = item['str_id']
        cursor.execute(sql, (provinceId, provinceName, uCodeNum, admissCode, collegeId, collegeName
                             , sort, isOld, codeChangeYear, str_id))
        # 错误函数

    def handle_error(self, failure, item, spider):
        print(failure)


class YzyCollegeScorelinePipline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = '''INSERT INTO yzy_college_scoreline (year,course,batch,batchName,uCode,chooseLevel
,lineDiff,minScore,avgScore,maxScore,lowSort,maxSort,enterNum,province_id)
 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''
        # 执行sql语句
        year = item['year']
        course = item['course']
        batch = item['batch']
        batchName = item['batchName']
        uCode = item['uCode']
        chooseLevel = item['chooseLevel']
        lineDiff = item['lineDiff']
        minScore = item['minScore']
        avgScore = item['avgScore']
        maxScore = item['maxScore']
        lowSort = item['lowSort']
        maxSort = item['maxSort']
        enterNum = item['enterNum']
        province_id = item['province_id']
        cursor.execute(sql, (year, course, batch, batchName, uCode, chooseLevel
                             , lineDiff, minScore, avgScore, maxScore, lowSort, maxSort, enterNum,
                             province_id))
        # 错误函数

    def handle_error(self, failure, item, spider):
        print(failure)


class YzyMajorScorelinePipline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = '''INSERT INTO yzy_major_scoreline (year,course,batch,batchName,uCode,chooseLevel
,lineDiff,minScore,avgScore,maxScore,lowSort,maxSort,enterNum,countOfZJZY,province_id,majorCode,professionName,professionCode
,remarks)
 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''
        # 执行sql语句
        year = item['year']
        course = item['course']
        batch = item['batch']
        batchName = item['batchName']
        uCode = item['uCode']
        chooseLevel = item['chooseLevel']
        lineDiff = item['lineDiff']
        minScore = item['minScore']
        avgScore = item['avgScore']
        maxScore = item['maxScore']
        lowSort = item['lowSort']
        maxSort = item['maxSort']
        enterNum = item['enterNum']
        countOfZJZY = item['countOfZJZY']
        majorCode = item['majorCode']
        professionName = item['professionName']
        professionCode = item['professionCode']
        remarks = item['remarks']
        province_id = item['province_id']
        cursor.execute(sql, (year, course, batch, batchName, uCode, chooseLevel
                             , lineDiff, minScore, avgScore, maxScore, lowSort, maxSort, enterNum, countOfZJZY,
                             province_id, majorCode, professionName, professionCode
                             , remarks))
        # 错误函数

    def handle_error(self, failure, item, spider):
        print(failure)


class YzyMajorPipline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

        # 处理sql函数

    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = '''INSERT INTO yzy_major (code,name,grade,category,category_code,subcategory
    ,subcategory_code)
     VALUES (%s,%s,%s,%s,%s,%s,%s)
    '''
        # 执行sql语句
        code = item['major_code']
        name = item['major_name']
        grade = item['grade']
        category = item['category_name']
        category_code = item['category_code']
        subcategory = item['subcategory_name']
        subcategory_code = item['subcategory_code']

        cursor.execute(sql, (code, name, grade, category, category_code, subcategory
                             , subcategory_code))
        # 错误函数

    #
    #     def insert_into(self, cursor, item):
    #         # 创建sql语句
    #         sql = '''INSERT INTO yzy_major_details (courses,description,employment,inherit_secondary_vocational,inherit_undergraduate
    # ,job_qualification_certificate,knowledge,major_name,major_code,grade,schooling_time,degree)
    #      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    #     '''
    #         # 执行sql语句
    #         code = item['major_code']
    #         name = item['major_name']
    #         grade = item['grade']
    #         courses = item['courses']
    #         description = item['description']
    #         employment = item['employment']
    #         inherit_secondary_vocational = item['inherit_secondary_vocational']
    #         inherit_undergraduate = item['inherit_undergraduate']
    #         job_qualification_certificate = item['job_qualification_certificate']
    #         knowledge = item['knowledge']
    #         schooling_time = item['schooling_time']
    #         degree = item['degree']
    #         cursor.execute(sql, (courses, description, employment, inherit_secondary_vocational, inherit_undergraduate
    #                              , job_qualification_certificate, knowledge, name, code, grade, schooling_time, degree))
    # 错误函数

    def handle_error(self, failure, item, spider):
        print(failure)


class YzyEnrollPlanPipline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = '''INSERT INTO yzy_enroll_plan_1 (year,courseType,batch,batchName,uCode,majorCode
,professionName,professionCode,planNum,cost,learnYear,province_id)
 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''
        # 执行sql语句
        year = item['year']
        courseType = item['courseType']
        batch = item['batch']
        batchName = item['batchName']
        uCode = item['uCode']
        majorCode = item['majorCode']
        professionName = item['professionName']
        professionCode = item['professionCode']
        planNum = item['planNum']
        cost = item['cost']
        learnYear = item['learnYear']
        province_id = item['province_id']
        cursor.execute(sql, (year, courseType, batch, batchName, uCode, majorCode
                             , professionName, professionCode, planNum, cost, learnYear, province_id))
        # 错误函数

    def handle_error(self, failure, item, spider):
        print(failure)


class YzyEnrollGuidePipline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = '''INSERT INTO enroll_guide (content,publish_date,title,college_id)
 VALUES (%s,%s,%s,%s)
'''
        # 执行sql语句
        content = item['content']
        publish_date = item['publish_date']
        title = item['title']
        college_id = item['college_id']
        cursor.execute(sql, (content, publish_date, title, college_id))
        # 错误函数

    def handle_error(self, failure, item, spider):
        print(failure)


class YzyCollegeMajorPipline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = '''insert into yzy_college_major(college_id,college_name,major_name,grade,yzy_college_id)
 values (%s,%s,%s,%s,%s)
'''
        # 执行sql语句
        college_name = item['college_name']
        major_name = item['major_name']
        grade = item['grade']
        college_id = item['college_id']
        yzy_college_id = item['yzy_college_id']
        cursor.execute(sql, (college_id, college_name, major_name, grade, yzy_college_id))
        # 错误函数

    def handle_error(self, failure, item, spider):
        print(failure)
