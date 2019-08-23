"""
@version:1.0
@author: endaqa
@file major_run.py
@time 2019/8/21 17:52
"""
# 中国科教网专业排名数据
import pandas as pd
import requests, pymysql, re
from lxml import etree
from urllib.parse import quote

db = pymysql.connect(host='39.104.137.32', user="ladin", port=45853, passwd='8yMCy9ikODmo$IJ%', db="shcool",
                     charset="utf8")
cursor = db.cursor()
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


def search(major_agv):
    major_agv = quote(major_agv, 'utf-8')
    url = f'http://www.nseac.com/plus/search.php?kwtype=0&keyword={major_agv}&searchtype=title'
    print(url)
    ht = requests.get(url, headers=head)
    if ht.status_code == 200:
        xpath_data = etree.HTML(ht.text)
        major_title = xpath_data.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/h3/a/text()')
        major_url = xpath_data.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/h3/a/@href')
        print(major_title)
        if major_title:
            if '18' in major_title[0]:
                return major_url[0]
        else:
            return 0

    else:
        return 1


def major_run(major_url, major):
    hts = requests.get(major_url, headers=head)
    if hts.status_code == 200:
        hts.encoding = 'utf-8'
        # print(hts.text)
        # major_xpath = etree.HTML(hts.text)
        # rank = major_xpath.xpath('/html/body/div[4]/div/div[1]/div[1]/table[1]/tbody/tr/td/center/div/table/tbody/tr/td[1]/text()')
        school_name = re.findall('target="_blank">(.*?)</a></td><', hts.text)
        # school_name = major_xpath.xpath('/html/body/div[4]/div/div[1]/div[1]/table[1]/tbody/tr/td/center/div/table/tbody/tr/td[2]/a/text()')
        # rank = re.findall('td class="neirong3">(\d)</td><td class="neirong4">',hts.text)
        # return rnak,school_name
        mysql_run(school_name, major)
    return 0


def mysql_run(school_name, major):
    print(school_name)
    for i in range(0, len(school_name)):
        sql = '''INSERT INTO major_rank2018(Rank,School,Major) VALUES ('%s','%s','%s')''' % (
            str(i + 1), school_name[i], major)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print('存储成功~！')

        except:
            # 如果发生错误则回滚
            db.rollback()
            print('存储失败已回滚！！')


def main():
    data_major = pd.read_csv('major.csv')
    major_list = data_major['Major']
    for i in major_list:

        major_url = search(i)
        print(major_url)
        if 'www' in str(major_url):
            state = major_run(major_url, i)
        else:
            print(i)


if __name__ == '__main__':
    main()
