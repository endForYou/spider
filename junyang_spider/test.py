"""
@version:1.0
@author: endaqa
@file test.py
@time 2019/11/8 11:35
"""
# import pymysql
#
# db = pymysql.connect(host="39.104.123.45",
#                      user="resource",
#                      password="vX1+U4N7HVZaiUhHQkV+oIOyHTw=",
#                      port=3306,
#                      database="dbresource",
#                      charset="utf8",
#                      use_unicode=True)
# cursor = db.cursor()
# print(cursor)
#
from fontTools.ttLib import TTFont

font = TTFont('cn_5.woff')
font.saveXML('./cn_5.xml')
