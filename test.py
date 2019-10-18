"""
@version:1.0
@author: endaqa
@file test.py
@time 2019/10/17 9:48
"""

import requests
from bs4 import BeautifulSoup as bs
import oss2
import sys
import re
import pymysql
import asyncio

base_url = "https://www.ewt360.com"
auth = oss2.Auth("LTAIEM8fuHovpucG", "dPx0vh9DtoYmJa7YemjcdknqIVLUev")

# endpoint = "http://oss-cn-huhehaote-internal.aliyuncs.com"
# Public endpoint
public_endpoint = "http://oss-cn-huhehaote.aliyuncs.com"
# Your bucket name
bucket_name = "fdpaperfile"
bucket = oss2.Bucket(auth, public_endpoint, bucket_name)


def crawl_paper_detail():
    upload_file_to_oss()


async def upload_file_to_oss(file_name, file):
    bucket.put_object(file_name, file)


async def main():
    list1 = []
    for i in (1, 2):
        list1.append(upload_file_to_oss("test%s" % i + "png", "test%s" % i + "png"))
        await asyncio.gather(*list1)


asyncio.run(main())
