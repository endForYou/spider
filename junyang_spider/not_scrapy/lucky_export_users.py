import csv
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.blocking import BlockingScheduler

from junyang_spider.libs.mail import Mail
import pymysql.cursors
import datetime

mail = Mail()


def export_file():
    db = pymysql.connect(user="root", password="junyang_admin",
                         host="47.122.6.171", port=3306,
                         charset="utf8",
                         db="destiny-calendar")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # print(datetime.datetime.now().date())
    delta = datetime.timedelta(days=1)
    now_day = datetime.datetime.now().date()
    yesterday = (datetime.datetime.now() - delta).date()
    date1 = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    date2 = now_day.strftime("%Y-%m-%d %H:%M:%S")
    sql = "select * from user where experience_activated_date_time>=%s and experience_activated_date_time <%s"

    cursor.execute(sql, (date1, date2))
    res = cursor.fetchall()
    file_path = str(now_day) + "注册用户数据.csv"
    out = open(file_path, "a", newline="", encoding="utf-8")
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(
        ["姓名", "注册时间", "电话号码"])
    for data in res:

        experience_activated_date_time = data['experience_activated_date_time'].strftime("%Y-%m-%d %H:%M:%S")
        name = data['name']
        phone_number = data['phone_number']
        csv_write.writerow(
            [ name,experience_activated_date_time,phone_number])
    # print(res)
    out.close()
    mail.send_to_contains_attach(subject="luck用户注册数据", attachments=file_path)
    cursor.close()
    db.close()


if __name__ == '__main__':
    conf = {
        'host': "159.75.224.137",
        'port': 6399,
        'password': "rYa+wq10dFTWzYz8FeZgsWRygyKfLKULSRdKfRnEgSk=",
        # 'decode_responses': True
    }
    # # # executors = {
    # # #     'default': ThreadPoolExecutor(10),  # 默认线程数
    # # #     'processpool': ProcessPoolExecutor(3)  # 默认进程
    # # # }
    jobstores = {
        'redis': RedisJobStore(db=3, **conf),

    }
    scheduler = BlockingScheduler(jobstores=jobstores, timezone='Asia/Shanghai')
    scheduler.add_job(export_file, 'cron', jobstore='redis', name="lucky", hour=10, minute=35, replace_existing=True)

    scheduler.start()
