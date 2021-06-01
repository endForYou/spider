"""
@version:1.0
@author: endaqa
@file my_apscheduler.py
@time 2020/9/29 16:31
"""
import os

import imgkit
import oss2
import redis
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import json
import requests
from apscheduler.jobstores.redis import *
from junyang_spider.libs.db_by_ssh import DBSSHHelper
from hashlib import md5
from bs4 import BeautifulSoup as bs
import urllib.parse
import time
import re


def update_article_info():
    url = "https://xwapp.moe.gov.cn/api/home/homeindex?page=1"
    res = requests.get(url)
    items = res.json()['data']['items']
    my_redis = redis.StrictRedis(db=2, host="42.194.210.56", port=6399,
                                 password="junyang@139", decode_responses=True)
    params = []
    # 爬取数据
    for item in items:

        title = item['title']
        title_md5 = md5(title.encode("utf-8")).hexdigest()

        if not my_redis.hexists('article_info', title_md5):
            path = item['path']
            create_time = item['publishTime']
            my_redis.hset('article_info', title_md5, create_time + title)
            picture = item['coverUrl1'].split("?x-oss-process")[0]
            content = requests.get(path).json()['article']['content']
            params.append({
                'create_time': create_time,
                'content': content,
                'picture': picture,
                'title': title

            })

    # 写入数据库
    if params:
        insert_data(params)


def update_top_search():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }

    # 更新网络热搜
    network_hot_search_url = "https://voice.baidu.com/activity/gaokao?page=collegeExam&tabname=tabHotList"
    res = requests.get(network_hot_search_url, headers=headers)

    soup = bs(res.text, "lxml")
    network_hot_search_params = []
    network_hot_search_items = soup.select("div['disable-link'='0'] > div > a")

    for network_hot_search_item in network_hot_search_items:
        title = network_hot_search_item.select_one("span.content__tJIHN.c-line-clamp1").get_text()
        browse_count = network_hot_search_item.select_one("span.num__15ubp.c-color").get_text()
        url = "https://www.baidu.com/s?word=%s&sa=os_collegeExam" % urllib.parse.quote(title)
        network_hot_search_params.append({
            'browse_count': browse_count,
            'name': title,
            'url': url,

        })

    # 更新院校热搜
    # 总共2200左右，所以一共有22页
    college_hot_search_url = "https://voice.baidu.com/api/commonkvapi"
    colleges = get_colleges()
    college_hot_search_params = []
    for page in range(1, 23):
        request_params = {
            "aid": "gaokao",
            "data":
                '{"trendList.tabs.0.list": {"descId": 22, "param": {"pageNum": %s, "pageSize": 100, "province": "全国"}}}' % page

        }
        # print(request_params)
        # headers["content-type"] = "application/json; charset=UTF-8"
        # print(request_params)
        res = requests.get(college_hot_search_url, headers=headers, params=request_params)
        college_hot_search_result_list = res.json()['data']['trendList.tabs.0.list']
        # print(college_hot_search_result_list)
        for college_obj in college_hot_search_result_list:
            name = college_obj['content'].replace("（", "(").replace("）", ")")
            num = college_obj['num']
            if name == "华北电力大学":
                name = "华北电力大学(北京)"
            if name not in colleges:
                name = name.replace("民办", "")
            if name not in colleges:
                continue
            else:
                college_id = colleges[name]
                college_hot_search_params.append({
                    'browse_count': num,
                    'name': name,
                    'time_dimension': 0,
                    'college_id': college_id

                })
        time.sleep(1)

    # # 更新专业热搜
    major_hot_search_url = "https://voice.baidu.com/api/commonkvapi"
    majors = get_majors()
    major_hot_search_params = []
    for page in range(1, 13):
        request_params = {
            "aid": "gaokao",
            "data":
                '{"trendList.tabs.1.list": {"descId": 23, "param": {"pageNum": %s, "pageSize": 100, "province": "全国"}}}' % page

        }
        # print(request_params)
        # headers["content-type"] = "application/json; charset=UTF-8"
        # print(request_params)
        res = requests.get(major_hot_search_url, headers=headers, params=request_params)
        # print(res.json())
        major_hot_search_result_list = res.json()['data']['trendList.tabs.1.list']
        for major_obj in major_hot_search_result_list:
            content = major_obj['content']
            education = major_obj['education']
            num = major_obj['num']
            # print(content, education)
            major_name = content.split("专业")[0]
            if education == "本科":
                grade = 0
            else:
                grade = 1
            if major_name in majors[grade].keys():
                major_id = majors[grade][major_name]
                major_hot_search_params.append({
                    'browse_count': num,
                    'name': content,
                    'time_dimension': 0,
                    'major_id': major_id

                })
            else:
                continue
        time.sleep(1)

    url = "https://voice.baidu.com/activity/gaokao?page=collegeExam&tabname=tabBigData&subtabname=collegeRank"
    res = requests.get(url, headers=headers)
    # print(res.text)
    datas = re.search("data\[\"tplData\"\] =(.*)data\[\"asyncConfig\"\]", res.text, re.DOTALL).group(1).replace(";",
                                                                                                                "").replace(
        "null", "None")

    tmp_dict = eval(datas)
    college_list = tmp_dict['trend']['list'][1]['list'][0]['list']
    for college in college_list:
        name = college['key'].replace("（", "(").replace("）", ")")
        num = college['value']
        print(name, num)
        if name == "华北电力大学":
            name = "华北电力大学(北京)"
        if name not in colleges:
            name = name.replace("民办", "")
        if name not in colleges:
            continue
        else:
            college_id = colleges[name]
            college_hot_search_params.append({
                'browse_count': num,
                'name': name,
                'time_dimension': 1,
                'college_id': college_id

            })
    major_list = tmp_dict['trend']['list'][1]['list'][1]['list']
    for major in major_list:

        content = major['key']

        num = major['value']
        # print(content, education)
        major_name = content.split("专业")[0]
        # print(content,major_name)
        if major_name in majors[0].keys():
            major_id = majors[0][major_name]
            major_hot_search_params.append({
                'browse_count': num,
                'name': content,
                'time_dimension': 1,
                'major_id': major_id

            })
        else:
            continue
    #
    if network_hot_search_params:
        insert_into_network_hot_search(network_hot_search_params)
    if college_hot_search_params:
        insert_into_college_hot_search(college_hot_search_params)
    if major_hot_search_params:
        insert_into_major_hot_search(major_hot_search_params)


def crawl_hunan_policy():
    url = "https://www.hneeb.cn/hnxxg/1/38/list.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    my_redis = redis.StrictRedis(db=2, host="42.194.210.56", port=6399,
                                 password="junyang@139", decode_responses=True)
    res = requests.get(url, headers=headers)
    soup = bs(res.text, "lxml")
    li_list = soup.select('div.zklb_list li')
    params = []
    base_url = "https://www.hneeb.cn/hnxxg/1/38/"
    for li in li_list:
        title = li.select_one("a").get_text()
        title_md5 = md5(title.encode("utf-8")).hexdigest()
        if not my_redis.hexists('province_policy', title_md5):
            url = base_url + li.select_one("a").get("href")
            create_time = li.select_one("span").text.replace("【", "").replace("】", "")
            my_redis.hset('province_policy', title_md5, create_time + title)
            params.append({
                "title": title,
                "link": url,
                "create_time": create_time,
                "province_id": 430000
            })
    if params:
        insert_into_province_policy(params)


def crawl_gd_policy():
    url = "http://eea.gd.gov.cn/ptgk/index.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    my_redis = redis.StrictRedis(db=2, host="42.194.210.56", port=6399,
                                 password="junyang@139", decode_responses=True)
    res = requests.get(url, headers=headers)
    soup = bs(res.text, "lxml")
    li_list = soup.select('div.content > ul.list > li')
    params = []
    for li in li_list:
        title = li.select_one("a").get_text()
        title_md5 = md5(title.encode("utf-8")).hexdigest()
        if not my_redis.hexists('province_policy', title_md5):
            url = li.select_one("a").get("href")
            create_time = li.select_one("span.time").text
            my_redis.hset('province_policy', title_md5, create_time + title)
            params.append({
                "title": title,
                "link": url,
                "create_time": create_time,
                "province_id": 440000
            })
    if params:
        insert_into_province_policy(params)


def crawl_hb_policy():
    url = "http://zsxx.e21.cn/e21html/zhaosheng/listihszbkxth1.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    my_redis = redis.StrictRedis(db=2, host="42.194.210.56", port=6399,
                                 password="junyang@139", decode_responses=True)
    res = requests.get(url, headers=headers)

    soup = bs(res.content.decode("gbk"), "lxml")
    li_list = soup.select("[width='700'] tr")

    params = []
    for li in li_list[0:-1]:
        title = li.select_one("a").get_text()
        title_md5 = md5(title.encode("utf-8")).hexdigest()
        # print(title)
        if not my_redis.hexists('province_policy', title_md5):
            url = "http://zsxx.e21.cn/" + li.select_one("a").get("href")
            create_time = li.select_one("td.gray12").text
            # print(url,create_time)
            print(url)
            my_redis.hset('province_policy', title_md5, create_time + title)
            params.append({
                "title": title,
                "link": url,
                "create_time": create_time,
                "province_id": 420000
            })
    if params:
        insert_into_province_policy(params)


def crawl_fj_policy():
    url = "https://www.eeafj.cn/gkptgkgsgg/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    my_redis = redis.StrictRedis(db=2, host="42.194.210.56", port=6399,
                                 password="junyang@139", decode_responses=True)
    res = requests.get(url, headers=headers)

    soup = bs(res.content.decode("UTF-8"), "lxml")
    # print(soup)
    li_list = soup.select("li a")
    year = str(datetime.now().year)
    params = []
    for li in li_list:
        title = li.get("title")
        # print(title)
        title_md5 = md5(title.encode("utf-8")).hexdigest()
        # print(title)
        if not my_redis.hexists('province_policy', title_md5):
            url = li.get("href")
            create_time = year + "-" + li.select_one("span").text.replace("[", "").replace("]", "")
            # print(url,create_time)
            # print(url,create_time)
            my_redis.hset('province_policy', title_md5, create_time + title)
            params.append({
                "title": title,
                "link": url,
                "create_time": create_time,
                "province_id": 350000
            })
    if params:
        insert_into_province_policy(params)


def insert_into_province_policy(data_list):
    insert_sql = '''
    insert into province_policy(create_time,insert_time,link,province_id,title
    ) values (%s,%s,%s,%s,%s)
    '''
    db_helper = DBSSHHelper()
    db_helper.connection_database(db="oms")
    params = []
    # 先删除数据
    insert_time = datetime.now()
    print(insert_time)
    for data in data_list:
        title = data['title']
        link = data['link']
        create_time = data['create_time']
        province_id = data['province_id']
        params.append((create_time, insert_time, link, province_id, title))
    # print(params)
    result = db_helper.execute_many(insert_sql, params)
    db_helper.close_database()
    if result:
        print("插入province_policy表成功")
    else:
        print("插入失败")


def insert_into_college_hot_search(data_list):
    insert_sql = '''
    insert into college_top_search(browse_count,name,time_dimension,college_id
    ) values (%s,%s,%s,%s)
    '''
    db_helper = DBSSHHelper()
    db_helper.connection_database(db="volunteer")
    params = []
    # 先删除数据
    db_helper.execute_one("delete from college_top_search")
    for data in data_list:
        browse_count = data['browse_count']
        name = data['name']
        time_dimension = data['time_dimension']
        college_id = data['college_id']

        params.append((browse_count, name, time_dimension, college_id))
    # print(params)
    result = db_helper.execute_many(insert_sql, params)
    db_helper.close_database()
    if result:
        print("插入college_top_search数据库成功")
    else:
        print("插入失败")


def insert_into_major_hot_search(data_list):
    insert_sql = '''
    insert into major_top_search(browse_count,name,time_dimension,major_id
    ) values (%s,%s,%s,%s)
    '''
    db_helper = DBSSHHelper()
    db_helper.connection_database(db="volunteer")
    params = []
    # 先删除数据
    db_helper.execute_one("delete from major_top_search")
    for data in data_list:
        browse_count = data['browse_count']
        name = data['name']
        time_dimension = data['time_dimension']
        major_id = data['major_id']

        params.append((browse_count, name, time_dimension, major_id))
    # print(params)
    result = db_helper.execute_many(insert_sql, params)
    db_helper.close_database()
    if result:
        print("插入major_top_search数据库成功")
    else:
        print("插入失败")


def insert_into_network_hot_search(data_list):
    insert_sql = '''
    insert into network_top_search(browse_count,name,url
    ) values (%s,%s,%s)
    '''
    db_helper = DBSSHHelper()
    db_helper.connection_database(db="volunteer")
    params = []
    # 先删除数据
    db_helper.execute_one("delete from network_top_search")
    for data in data_list:
        browse_count = data['browse_count']
        name = data['name']
        url = data['url']

        params.append((browse_count, name, url))
    # print(params)
    result = db_helper.execute_many(insert_sql, params)
    db_helper.close_database()
    if result:
        print("插入network_top_search数据库成功")
    else:
        print("插入失败")


def insert_data(data_list):
    insert_sql = '''
    insert into article_info(collection_number,comment_number,content,create_time,file_type,picture,play_number,
    read_number,recommend_number,release_time,status,title,create_use_id,module_id,special_topic_info_id
    ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    db_helper = DBSSHHelper()
    db_helper.connection_database()
    params = []
    collection_number = 0
    comment_number = 0
    play_number = 0
    read_number = 0
    recommend_number = 0
    file_type = 0
    status = 1
    create_use_id = 4421
    module_id = 8
    special_topic_info_id = 637593
    for data in data_list:
        release_time = data['create_time']
        create_time = data['create_time']
        content = data['content']
        picture = data['picture']
        title = data['title']
        params.append((collection_number, comment_number, content, create_time, file_type, picture, play_number,
                       read_number, recommend_number, release_time, status, title, create_use_id, module_id,
                       special_topic_info_id
                       ))
    # print(params)
    result = db_helper.execute_many(insert_sql, params)
    db_helper.close_database()
    print(params)
    print(result)
    if result:
        print("插入数据库成功")
    else:
        print("插入失败")


def get_majors():
    db_helper = DBSSHHelper()
    db_helper.connection_database(db="volunteer")
    sql = "select id,name,grade from major"
    res = db_helper.select_all(sql)
    result_dict = {}
    for data in res:
        grade = data['grade']
        ids = data['id']
        name = data['name']
        if grade not in result_dict.keys():
            result_dict[grade] = {}
        if name not in result_dict[grade].keys():
            result_dict[grade][name] = ids
    db_helper.close_database()
    return result_dict


def get_colleges():
    db_helper = DBSSHHelper()
    db_helper.connection_database(db="volunteer")
    sql = "select id,name from college"
    res = db_helper.select_all(sql)
    result_dict = {}
    for data in res:
        ids = data['id']
        name = data['name']
        result_dict[name] = ids
    db_helper.close_database()
    return result_dict


def update_province_policy_linux():
    auth = oss2.Auth('LTAI4Fg3MtymYqu8kuqe8vDU', 'mBrPMusVDYr9P4q3dIjHOW6xTexdbA')
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, 'http://oss-cn-huhehaote.aliyuncs.com', 'zhiya-data')
    db_helper = DBSSHHelper()
    db_helper.connection_database(db="oms")
    sql = "select id,link from province_policy where  image_url is null"
    source_data = db_helper.select_all(sql)
    path_wkimg = "/usr/local/bin/wkhtmltoimage"
    cfg = imgkit.config(wkhtmltoimage=path_wkimg)
    update_sql = "update province_policy set image_url=%s where id=%s"
    for data in source_data:
        ids = data['id']
        link = data['link']
        image_name = "image/" + str(ids) + ".jpg"
        try:
            imgkit.from_url(link, image_name, config=cfg)
            bucket.put_object_from_file("oms/policy/" + str(ids) + ".jpg", image_name)
            db_helper.execute_one(update_sql, (
                "https://zhiya-data.oss-cn-huhehaote.aliyuncs.com/oms/policy/" + str(ids) + ".jpg", ids))
            os.remove(image_name)
        except BaseException as e:

            if os.path.exists(image_name):
                bucket.put_object_from_file("oms/policy/" + str(ids) + ".jpg", image_name)
                db_helper.execute_one(update_sql, (
                    "https://zhiya-data.oss-cn-huhehaote.aliyuncs.com/oms/policy/" + str(ids) + ".jpg", ids))
                os.remove(image_name)
    db_helper.close_database()


if __name__ == '__main__':
    # crawl_fj_policy()
    conf = {
        'host': "42.194.210.56",
        'port': 6399,

        'password': "junyang@139",
        # 'decode_responses': True
    }
    # executors = {
    #     'default': ThreadPoolExecutor(10),  # 默认线程数
    #     'processpool': ProcessPoolExecutor(3)  # 默认进程
    # }
    jobstores = {
        'redis': RedisJobStore(db=2, **conf),

    }
    #
    # # job_defaults = {
    # #     'coalesce': False,
    # #     'max_instances': 3
    # # }
    scheduler = BlockingScheduler(jobstores=jobstores)
    scheduler.add_job(update_article_info, 'cron', jobstore='redis', hour=8)
    scheduler.add_job(update_top_search, 'interval', jobstore='redis', days=7)
    scheduler.add_job(update_province_policy_linux, 'interval', jobstore='redis', minutes=30)
    scheduler.add_job(crawl_hunan_policy, 'cron', jobstore='redis', hour=8)
    scheduler.add_job(crawl_gd_policy, 'cron', jobstore='redis', hour=8)
    scheduler.add_job(crawl_hb_policy, 'cron', jobstore='redis', hour=8)
    scheduler.add_job(crawl_fj_policy, 'cron', jobstore='redis', hour=8)
    scheduler.start()
