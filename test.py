"""
@version:1.0
@author: endaqa
@file test.py
@time 2019/8/22 10:50
"""
import pymysql


class Parent(object):
    name = "jw"

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def print_name(self):
        print(self.name)


class Child(Parent):

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)


child = Child("jiewei")
child.print_name()
fcode = "34567"
item = {

}

print(f"select * from function where code like '{fcode[:2]}%' and code!={fcode}")

name = "Eric"
age = 74
doc = {
    "Id": 1,
    "Rid": 23,
    "CompanyName": "钧扬网络技术有限公司"
}
insert = f"insert into jobinfo19822({','.join(item.keys())}) values(" + ','.join(
    ['"{' + k + '}"' for k in item.keys()]) + ")"
doc = {k: pymysql.escape_string(v) if isinstance(v, str) else v for k, v in doc.items()}

sqltext = insert.format(**doc)
print(sqltext)
