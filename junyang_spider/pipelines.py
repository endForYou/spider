# -*- coding: utf-8 -*-
import pymysql, pymongo, re
from twisted.internet.threads import deferToThread
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
