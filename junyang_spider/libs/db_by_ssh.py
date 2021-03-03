"""
@version:1.0
@author: endaqa
@file db_by_ssh.py
@time 2020/7/13 15:57
"""
import traceback

import pymysql
from sshtunnel import SSHTunnelForwarder


# 通过SSH链接数据库
class DBSSHHelper:
    # 构造函数,初始化数据库连接
    def __init__(self):
        self.server = None
        self.my_config = None
        self.cursor = None

    # 连接数据库
    def connection_database(self, db="oms"):
        try:
            self.server = SSHTunnelForwarder(
                ssh_address_or_host=("42.194.215.214", 22),  # ssh跳转机的地址
                ssh_username="test_user",  # ssh的用户名
                ssh_pkey="D:\\file\personal\\key_file\\new_key\\id_rsa",  # ssh私钥地址
                # ssh_private_key_password="",  # ssh私钥密码
                # local_bind_address=("0.0.0.0", 10022),
                remote_bind_address=("rm-hp3ly1uji477469lcko.mysql.huhehaote.rds.aliyuncs.com", 3306))  # 数据库地址
            self.server.__enter__()
            self.my_config = pymysql.connect(
                user="dev",  # 数据库登录名
                passwd="Hbz8DLPUjTNqQn8fg+rsIEuqIxI=",  # 数据库密码
                host="127.0.0.1",  # 写死
                db=db,  # 数据库名称
                port=self.server.local_bind_port,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True)  # sql查询结果返回类型：DictCursor 为字典类型， 没有指定为 数组
            self.cursor = self.my_config.cursor()
        except Exception as e:  # 捕捉异常，并打印
            traceback.print_exc()
            return False
        return True

    # 关闭数据库
    def close_database(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.cursor:
            self.cursor.close()
        if self.my_config:
            self.my_config.close()
        if self.server:
            self.server.__exit__()
        return True

    # 查询数据,返回集合
    def select_all(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def execute_one(self, sql, params=None):
        if params:
            result = self.cursor.execute(sql, params)
        else:
            result = self.cursor.execute(sql)
        return result

    def execute_many(self, sql, params):
        result = self.cursor.executemany(sql, params)

        return result

    # 查询数据，返回单个
    def select_one(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result


if __name__ == "__main__":
    db_helper = DBSSHHelper()
    db_helper.connection_database()

    results = db_helper.select_all("select * from province limit 10")
    print(results)

    # result = db_helper.select_one("select * from client_customers where id=131")
    # print(result)
    db_helper.close_database()
