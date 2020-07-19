"""
@version:1.0
@author: endaqa
@file execute_js.py
@time 2020/3/4 9:42
"""

import execjs
import os
js_dir='/Users/end/PycharmProjects/junyang_spider/junyang_spider/libs/'
#js_dir = "E:\\project\\git_project\\junyang_spider\\junyang_spider\\libs\\"
with open(os.path.join(js_dir, "common_service.js"), "r", encoding="utf8") as f:
    js_code = f.read()
# print(js_code)
ctx = execjs.compile(js_code)


def encrypt_data(data):
    res = ctx.call('service.youzyEpt', data)
    return res
