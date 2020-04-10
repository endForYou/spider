"""
@version:1.0
@author: endaqa
@file ewt_career_planning_spider.py
@time 2019/11/11 15:17
"""

import requests
from bs4 import BeautifulSoup as bs
import oss2
import sys
import re
import pymysql
import asyncio
import csv

base_url = "https://ewt360.com"

# auth = oss2.Auth("LTAIEM8fuHovpucG", "dPx0vh9DtoYmJa7YemjcdknqIVLUev")
#
# # endpoint = "http://oss-cn-huhehaote-internal.aliyuncs.com"
# # Public endpoint
# public_endpoint = "http://oss-cn-huhehaote.aliyuncs.com"
# # Your bucket name
# bucket_name = "fdpaperfile"
# bucket = oss2.Bucket(auth, public_endpoint, bucket_name)
# db_config = {
#     "host": '39.104.123.45',
#     "name": 'dbresource',
#     "user": 'resource',
#     "password": 'vX1+U4N7HVZaiUhHQkV+oIOyHTw=',
#     "charset": 'utf8'
# }
#
# db = pymysql.connect(host=db_config['host'], user=db_config['user'], database=db_config['name'],
#                      password=db_config['password'], charset=db_config['charset'], autocommit=True)
# cursor = db.cursor()
#
# insert_sql = "insert into paper_file(data_category,data_type,version,subject,grade,upload_time,url) values(%s,%s,%s,%s,%s,%s,%s)"
#
# out = open("ewt_career_planning.csv", 'a', newline='', encoding='utf-8')
# head = ["file_name", "province", ]
# csv_write = csv.writer(out, dialect='excel')
# csv_write.writerow(head)
db = pymysql.connect(host="39.104.123.45", user="root", password="bqbXRXlDAZHZtF1928=", database="dbresource",
                     charset="utf8", autocommit=True)
cursor = db.cursor(pymysql.cursors.DictCursor)


def crawl_paper_list():
    headers = {
        'Cookie': "big_data_cookie_id=f0ac135c-dfee-97e7-5f2e-695074e1b5a0%7C1566979046182; Hm_mstid_=798863147595853; _ga=GA1.2.2147104404.1566979047; Hm_lvt_5261308991055a39373a5ccf8edd3695=1571638418,1572593277,1573727355; Hm_lvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1585121988; _gid=GA1.2.2031544076.1585121989; UserID=15045901; user=tk=15045901-1-2a3b6ffe38dba701&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uSHxbNR88L3AbuMOeE3SHGJEZ7bzkjdADrRhDRRHba8Es%0AnF+TguV5PP1QBwPQgMhroZbjTUMtJQ/5jaiAohGJYCXHqme7s1JSeAOh0l/FufG4lGc2c4pYDg==; ewt_user=tk=15045901-1-2a3b6ffe38dba701&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uSHxbNR88L3AbuMOeE3SHGJEZ7bzkjdADrRhDRRHba8Es%0AnF+TguV5PP1QBwPQgMhroZbjTUMtJQ/5jaiAohGJYCXHqme7s1JSeAOh0l/FufG4lGc2c4pYDg==; token=15045901-1-2a3b6ffe38dba701; Hm_lvt_=1585121988,1585121994,1585122014; Hm_lpvt_=1585122523; Hm_lpvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1585122524",
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "8c2edf16-39c6-48d8-94c5-c7142412291f,1a9b8e21-c718-4aa1-a454-b237d6687ee5",
        'Host': "www.ewt360.com",
        'Accept-Encoding': "gzip, deflate",
        'cache-control': "no-cache"
    }
    url = base_url + "/ApplyNews/NewsList"
    type_dic = {
        "13": "生涯认知",
        "7": "专业与职业",
        "6": "生涯动态",
        "4": "排行榜",
        "2": "志愿填报",
    }
    insert_into_sql = "insert into career_planning_article(categorys,title,upload_time,html_content,url) values (%s,%s,%s,%s,%s)"
    for k, v in type_dic.items():
        if k == "2":
            childNum = 3
        else:
            childNum = 0
        querystring = {"typeId": k, "childNum": childNum}
        # response = requests.request("GET", url, headers=headers, params=querystring)
        # if response.status_code == 200:
        #     soup = bs(response.text, "lxml")
        #     text = soup.select_one(".page div:nth-of-type(1)").get_text().strip()
        #     # print(text)
        #     #page_count = int(re.findall("1/(.*)页", text)[0].split("页")[0])
        #     print(page_count)
        page_count = 4
        for page in range(1, page_count + 1):
            querystring = {"typeId": k, "childNum": childNum, "page": page}
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.status_code == 200:
                soup = bs(response.text, "lxml")
                items = soup.select("div.mnsTitle")
                for item in items:
                    href = item.select_one("h1 a").attrs['href']
                    title = item.select_one("h1 a").get_text()
                    upload_time = item.select_one("span.mnsS").get_text()
                    detail_url = base_url + href
                    response = requests.request("GET", detail_url, headers=headers)
                    if response.status_code == 200:
                        soup = bs(response.text, "lxml")
                        # print(response.text)
                        html_content = str(soup.select_one("section").extract())

                        # print(v, title, upload_time, detail_url)
                        # print(html_content)
                        cursor.execute(insert_into_sql, (v, title, upload_time, html_content, detail_url))

            else:
                print(url)
            # for item in items:
            #     # href = item.select_one("a").attrs['href']
            #     name = item.select_one("a").get_text().strip()
            #     print(name)
            # detail_url = base_url + href
            # print(detail_url)
            # crawl_paper_detail(detail_url, headers)


#
# def crawl_detail(url, headers):
#     response = requests.request("GET", url, headers=headers)
#     if response.status_code == 200:
#         soup = bs(response.text, "lxml")
#         # print(response.text)
#         content = soup.select_one("section")
#
#         print(content)
#         # # file = result[1]
#         # asyncio.gather()
#         # print(result)
#         # cursor.execute(insert_sql, (data_category, data_type, version, subject, grade, upload_time, data_category))
#         # print(file_url)
#     else:
#         print(url)


# def get_file_url(url, headers):
#     headers['Referer'] = url
#     file_url_response = requests.request("GET", url, headers=headers, allow_redirects=False)
#     result = re.findall('href="(.*)">', file_url_response.text)
#     final_file_url = "https:" + result[0]
#     # file = requests.get(final_file_url)
#     # file_name = file.headers['Content-Disposition'].split("filename=")[1]
#     # end_url = "https://fdpaperfile.oss-cn-huhehaote.aliyuncs.com/" + file_name
#     # return
#     return final_file_url


# async def upload_file_to_oss(file_name, file, data_category, data_type, version, subject, grade, upload_time):
#     bucket.put_object(file_name, file)
#     end_url = "https://fdpaperfile.oss-cn-huhehaote.aliyuncs.com/" + file_name
#     cursor.execute(insert_sql, (data_category, data_type, version, subject, grade, upload_time, end_url))


# def write_to_mysql():


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
