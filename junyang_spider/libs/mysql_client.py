"""
@version:1.0
@author: endaqa
@file mysql_client.py
@time 2020/7/14 15:57
"""

import pymysql
from DBUtils.PooledDB import PooledDB

'''
连接池
'''


class MysqlPool(object):

    def __init__(self):
        self.POOL = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host='39.104.123.45',
            port=3306,
            user='root',
            password='bqbXRXlDAZHZtF1928=',
            database='zhiyuan_new',
            charset='utf8'
        )

    def __new__(cls, *args, **kw):
        """
        启用单例模式
        :param args:
        :param kw:
        :return:
        """
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def connect(self):
        """
        启动连接
        :return:
        """
        conn = self.POOL.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return conn, cursor

    def connect_close(self, conn, cursor):
        """
        关闭连接
        :param conn:
        :param cursor:
        :return:
        """
        cursor.close()
        conn.close()

    def fetch_all(self, sql, args=None):
        """
        批量查询
        :param sql:
        :param args:
        :return:
        """
        conn, cursor = self.connect()

        cursor.execute(sql, args)
        record_list = cursor.fetchall()
        self.connect_close(conn, cursor)

        return record_list

    def fetch_one(self, sql, args):
        """
        查询单条数据
        :param sql:
        :param args:
        :return:
        """
        conn, cursor = self.connect()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        self.connect_close(conn, cursor)

        return result

    def execute_sql(self, sql, args=None):
        """
        执行sql
        :param sql:
        :param args:
        :return:
        """
        conn, cursor = self.connect()
        row = cursor.execute(sql, args)
        #print(args)
        conn.commit()
        self.connect_close(conn, cursor)
        return row

    def execute_many_sql(self, sql, args):
        """
        执行多条sql
        :param sql:
        :param args:
        :return:
        """
        conn, cursor = self.connect()
        row = cursor.executemany(sql, args)
        conn.commit()
        self.connect_close(conn, cursor)
        return row

    def get_proxys(self, number):
        sql = "select id,fail_count,proxy from  proxys where is_valid=1 limit 5"
        data_list = self.fetch_all(sql)
        return data_list

    def update_proxys_status(self, ):
        sql = "update proxys set is_valid=0 where fail_count=1"
        self.execute_sql(sql)

    def update_proxys_fail_count(self, proxy_id):
        sql = "update proxys set fail_count=fail_count+1 where id=%s"
        self.execute_sql(sql, proxy_id)

    def insert_proxys(self, **kwargs):
        sql = '''
        insert into proxys(proxy,fail_count,region,proxy_type,source,is_used,expiration_time,is_valid,operator) 
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        #print(kwargs,222222222222)
        proxy = kwargs['proxy']
        fail_count = kwargs['fail_count']
        region = kwargs['region']
        proxy_type = kwargs['proxy_type']
        source = kwargs['source']
        is_used = kwargs['is_used']
        expiration_time = kwargs['expiration_time']
        is_valid = kwargs['is_valid']
        operator = kwargs['operator']
        print(proxy, fail_count, region, proxy_type, source, is_used, expiration_time, is_valid, operator,1111111111111)
        self.execute_sql(sql,
                         (proxy, fail_count, region, proxy_type, source, is_used, expiration_time, is_valid, operator))
