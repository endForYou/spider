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

auth = oss2.Auth("LTAIEM8fuHovpucG", "dPx0vh9DtoYmJa7YemjcdknqIVLUev")

# endpoint = "http://oss-cn-huhehaote-internal.aliyuncs.com"
# Public endpoint
public_endpoint = "http://oss-cn-huhehaote.aliyuncs.com"
# Your bucket name
bucket_name = "fdcareer"
bucket = oss2.Bucket(auth, public_endpoint, bucket_name)
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
        'Cookie': "big_data_cookie_id=f0ac135c-dfee-97e7-5f2e-695074e1b5a0%7C1566979046182; Hm_mstid_=798863147595853; _ga=GA1.2.2147104404.1566979047; UserID=15045901; Hm_lvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1571106514,1571638418,1572593277; Hm_lvt_5261308991055a39373a5ccf8edd3695=1571106514,1571638418,1572593277; _gid=GA1.2.671273945.1573451862; ASP.NET_SessionId=e223oyvcd0uklr1q2utura1t; user=tk=15045901-1-bf33fbec39cd1a0e&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uSHxbNR88L3AbuMOeE3SHGJEZ7bzkjdADvG2Zi8TKVIvL%0AJ5txrZj9f4E6f2HVXC5SwrR4+tfa31++aCRUajQauc2azsvmHXky9DbsslEVHUptxoC7EmCUuw==; ewt_user=tk=15045901-1-bf33fbec39cd1a0e&info=FY6PmGnI2LPN+XQfS1m0Kt1V+mq4ym/uSHxbNR88L3AbuMOeE3SHGJEZ7bzkjdADvG2Zi8TKVIvL%0AJ5txrZj9f4E6f2HVXC5SwrR4+tfa31++aCRUajQauc2azsvmHXky9DbsslEVHUptxoC7EmCUuw==; token=15045901-1-bf33fbec39cd1a0e; Hm_lvt_=1573096946,1573451862,1573455714,1573463053; Hm_lpvt_=1573463079; Hm_lpvt_9f9b5bffee4cbc2aeda3d2bb3470e2f6=1573463079; Hm_lpvt_5261308991055a39373a5ccf8edd3695=1573463079",
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "8c2edf16-39c6-48d8-94c5-c7142412291f,1a9b8e21-c718-4aa1-a454-b237d6687ee5",
        'Host': "www.ewt360.com",
        'Accept-Encoding': "gzip, deflate",
        'cache-control': "no-cache"
    }
    url = base_url + "/apiapply/CareerNews"
    type_dic = {
        "13": "生涯认知",
        "7": "专业与职业",
        "6": "生涯动态",
        "4": "排行榜",
        "2": "志愿填报",
    }
    token = "15045901-2-c5aba5c766d7f7b5"
    insert_into_sql = "insert into career_planning_article_new(category,title,upload_time,html_content,cover,overview) values (%s,%s,%s,%s,%s,%s)"
    for k, v in type_dic.items():
        if k == "2":
            child_num = "3"
        else:
            child_num = "0"
        for page in (1, 2, 3):
            querystring = {"typeId": k, "childNum": child_num, "token": token, "page": page}
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.status_code == 200:
                data = response.json()
                record_list = data['data']['list']
                for record in record_list:
                    title = record['title']
                    upload_time = record['addtime']
                    image_path = record['imagepath']
                    overview = record['content']
                    ids = record['id']
                    querystring = {"id": ids, "referUrl": "TmV3Tm9ybWFNb3JlU3BlY2lhbGlzdGxWaWV3Q29udHJvbGxlcg=="}
                    detail_url = base_url + "/WebView/NewsDetail"
                    response = requests.request("GET", detail_url, headers=headers, params=querystring)
                    # print(response.status_code)
                    soup = bs(response.text, "lxml")
                    # print(response.text)
                    html_content = str(soup.select_one("section").extract())
                    # 过滤带关键字的文章

                    if html_content.find("E网通") != -1 or html_content.find("小E") != -1:
                        continue
                    # print(html_content)
                    cursor.execute(insert_into_sql, (v, title, upload_time, html_content, image_path, overview))

            #     print(url) for item in items:
            #         href = item.select_one("h1 a").attrs['href']
            #         title = item.select_one("h1 a").get_text()
            #         upload_time = item.select_one("span.mnsS").get_text()
            #         detail_url = base_url + href
            #         response = requests.request("GET", detail_url, headers=headers)
            #         if response.status_code == 200:
            #             soup = bs(response.text, "lxml")
            #             # print(response.text)
            #             html_content = str(soup.select_one("section").extract())
            #
            #             # print(v, title, upload_time, detail_url)
            #             # print(html_content)
            #             cursor.execute(insert_into_sql, (v, title, upload_time, html_content, detail_url))
            #
            # else:
            # for item in items:
            #     # href = item.select_one("a").attrs['href']
            #     name = item.select_one("a").get_text().strip()
            #     print(name)
            # detail_url = base_url + href
            # print(detail_url)
            # crawl_paper_detail(detail_url, headers)
            else:
                print(response.status_code)


if __name__ == "__main__":
    crawl_paper_list()
    cursor.close()
    db.close()
