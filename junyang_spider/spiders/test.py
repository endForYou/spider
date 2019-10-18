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
db_config = {
    "host": '39.104.123.45',
    "name": 'dbresource',
    "user": 'resource',
    "password": 'vX1+U4N7HVZaiUhHQkV+oIOyHTw=',
    "charset": 'utf8'
}

db = pymysql.connect(host=db_config['host'], user=db_config['user'], database=db_config['name'],
                     password=db_config['password'], charset=db_config['charset'], autocommit=True)
cursor = db.cursor()

insert_sql = "insert into paper_file(data_category,data_type,version,subject,grade,upload_time,url) values(%s,%s,%s,%s,%s,%s,%s)"


def crawl_paper_list():
    headers = {
        'Cookie': "big_data_cookie_id=f0ac135c-dfee-97e7-5f2e-695074e1b5a0%7C1566979046182; Hm_mstid_=798863147595853; _ga=GA1.2.2147104404.1566979047; Hm_lvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571106514; Hm_lvt_5261308991055a39373a5ccf8edd3695=1571106514; UserID=15045901; ASP.NET_SessionId=tjqzhmpvzeq10sklxvhqvu1n; PassWord=; PWLength=; IsRemember=; _gid=GA1.2.1140154414.1571387891; Hm_lvt_=1571213144,1571213386,1571387899,1571387901; Hm_lpvt_=1571391437; _gat=1; Hm_lpvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571391437; Hm_lpvt_5261308991055a39373a5ccf8edd3695=1571391437; user=tk=15045901-1-b7bdbd2b832484e9&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uT6MmsUKCjgTDefVWCnYBlq0EtD3A7o+MSCHkzbqcrMrB%0AOgrwDobbikj0RfsO4adRTe/1IeyPvEyMm/bgSlU1kn2W+17VYEgWjOsz8dL0FPlXgYgh52S5Rw==; ewt_user=tk=15045901-1-b7bdbd2b832484e9&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uT6MmsUKCjgTDefVWCnYBlq0EtD3A7o+MSCHkzbqcrMrB%0AOgrwDobbikj0RfsO4adRTe/1IeyPvEyMm/bgSlU1kn2W+17VYEgWjOsz8dL0FPlXgYgh52S5Rw==; token=15045901-1-b7bdbd2b832484e9",
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "8c2edf16-39c6-48d8-94c5-c7142412291f,1a9b8e21-c718-4aa1-a454-b237d6687ee5",
        'Host': "www.ewt360.com",
        'Accept-Encoding': "gzip, deflate",
        'cache-control': "no-cache"
    }
    url = base_url + "/Review/Lists"
    for page in range(1, 4296):
        querystring = {"page": "{page}".format(page=page)}
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            soup = bs(response.text, "lxml")
            items = soup.select("li.pngFix")
            for item in items:
                href = item.select_one("a").attrs['href']
                detail_url = base_url + href
                print(detail_url)
                crawl_paper_detail(detail_url, headers)
        else:
            print(url)


def crawl_paper_detail(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        soup = bs(response.text, "lxml")
        # print(response.text)

        data_category_list = soup.select_one("tr:nth-of-type(1) td").get_text().strip().split("：")
        if len(data_category_list) < 2:
            data_category = ""
        else:
            data_category = data_category_list[1]
        print(data_category)
        data_type_list = soup.select_one("tr:nth-of-type(2) td").get_text().strip().split("：")
        if len(data_type_list) < 2:
            data_type = ""
        else:
            data_type = data_type_list[1]
        version_list = soup.select_one("tr:nth-of-type(3) td:nth-of-type(1)").get_text().strip().split("：")
        if len(version_list) < 2:
            version = ""
        else:
            version = version_list[1]
        subject_list = soup.select_one("tr:nth-of-type(3) td:nth-of-type(2)").get_text().strip().split("：")
        if len(subject_list) < 2:
            subject = ""
        else:
            subject = subject_list[1]
        grade_list = soup.select_one("tr:nth-of-type(4) td:nth-of-type(1)").get_text().strip().split("：")
        if len(grade_list) < 2:
            grade = ""
        else:
            grade = grade_list[1]
        upload_time_list = soup.select_one("tr:nth-of-type(5) td:nth-of-type(1)").get_text().strip().split("：")
        if len(upload_time_list) < 2:
            upload_time = ""
        else:
            upload_time = upload_time_list[1]
        file_url = base_url + soup.select_one("tr:nth-of-type(5) td:nth-of-type(2) a").attrs['href'].strip()
        # print(file_url)
        result = get_file_url(file_url, headers)
        # end_url = result[0]
        # # file = result[1]
        # asyncio.gather()
        # print(result)
        cursor.execute(insert_sql, (data_category, data_type, version, subject, grade, upload_time, data_category))
        # print(file_url)
    else:
        print(url)


def get_file_url(url, headers):
    headers['Referer'] = url
    file_url_response = requests.request("GET", url, headers=headers, allow_redirects=False)
    result = re.findall('href="(.*)">', file_url_response.text)
    final_file_url = "https:" + result[0]
    file = requests.get(final_file_url)
    file_name = file.headers['Content-Disposition'].split("filename=")[1]
    end_url = "https://fdpaperfile.oss-cn-huhehaote.aliyuncs.com/" + file_name
    return end_url, file


async def upload_file_to_oss(file_name, file, data_category, data_type, version, subject, grade, upload_time):
    bucket.put_object(file_name, file)
    end_url = "https://fdpaperfile.oss-cn-huhehaote.aliyuncs.com/" + file_name
    cursor.execute(insert_sql, (data_category, data_type, version, subject, grade, upload_time, end_url))


def write_to_mysql():
    pass

# def percentage(consumed_bytes, total_bytes):
#     if total_bytes:
#         rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
#         print('\r{0}% '.format(rate), end='')
#
#         sys.stdout.flush()


# print(response.text)
#
# response = requests.request("GET", "https://www.ewt360.com/Review/Detail/132117", headers=headers)
#
# print(response.text)
if __name__ == "__main__":
    crawl_paper_list()
    cursor.close()
    db.close()
