import pymysql
from junyang_spider import settings


class DBConnection(object):
    def __init__(self):
        self._connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            # autocommit=True,
            use_unicode=True)
        self._cursor = self._connect.cursor(pymysql.cursors.DictCursor)

    def get_yzy_provinces(self):
        sql = "select ProvinceId  from yzy_province where Used=1"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        return result

    def get_colleges_enroll_code_from_db(self):
        # sql = "select provinceId,uCodeNum from yzy_college_enroll_code where provinceId in (select ProvinceId from yzy_province where Used=1)"
        sql = "select provinceId,uCodeNum from yzy_college_enroll_code where provinceId=850"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        return result

    def get_yzy_colleges(self):
        sql = "select DISTINCT yzy_college_id from yzy_college"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        return result

    def tear_down(self):
        self._cursor.close()
        self._connect.close()
