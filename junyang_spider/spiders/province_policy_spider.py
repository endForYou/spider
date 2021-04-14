"""
@version:1.0
@author: endaqa
@file province_policy_spider.py
@time 2021/4/13 17:34
"""
import redis
import requests
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup as bs
import datetime
from hashlib import md5
from junyang_spider.libs.db_by_ssh import DBSSHHelper


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
    base_url="https://www.hneeb.cn/hnxxg/1/38/"
    for li in li_list:
        title = li.select_one("a").get_text()
        title_md5 = md5(title.encode("utf-8")).hexdigest()
        if not my_redis.hexists('province_policy', title_md5):

            url = base_url+li.select_one("a").get("href")
            create_time = li.select_one("span").text.replace("【","").replace("】","")
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


def insert_into_province_policy(data_list):
    insert_sql = '''
    insert into province_policy(create_time,insert_time,link,province_id,title
    ) values (%s,%s,%s,%s,%s)
    '''
    db_helper = DBSSHHelper()
    db_helper.connection_database(db="oms")
    params = []
    # 先删除数据
    insert_time = datetime.datetime.now()
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


if __name__ == '__main__':
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

    scheduler.add_job(crawl_hunan_policy, 'cron', jobstore='redis', hour=8)
    scheduler.add_job(crawl_gd_policy, 'cron', jobstore='redis', hour=8)

    scheduler.start()
