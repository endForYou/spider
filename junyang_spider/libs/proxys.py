"""
@version:1.0
@author: endaqa
@file proxys.py
@time 2020/6/24 18:33
"""
import json

from junyang_spider.libs import WebRequest
from bs4 import BeautifulSoup
import random

from junyang_spider.libs.mysql_client import MysqlPool


class Proxy:
    def __init__(self):
        self.mysql_pool = MysqlPool()
        self.ip_list = []

    def __new__(cls, *args, **kw):
        """
        启用单例模式
        :param args:
        :param kw:
        :return:
        """
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    @staticmethod
    def get_random_proxy_from_constant_proxys():
        ip_list = [
            "1.196.116.90:40916", "60.172.83.221:28803", "60.189.126.131:31665", "117.69.244.142:28803",
            "125.120.200.133:27986", "222.133.167.188:13504",
            "119.132.68.38:28803", "221.203.128.243:28469"
        ]
        return random.choice(ip_list)

    def get_proxys_from_mysql(self, number):
        # 先看缓存的ip_list是否是空
        # if not self.ip_list:
        proxys_list = self.mysql_pool.get_proxys(number)
        if not proxys_list:
            self.acquire_proxy_to_mysql(number)
            proxys_list = self.mysql_pool.get_proxys(number)
        elif len(proxys_list) < number:
            self.acquire_proxy_to_mysql(number - len(proxys_list))
            proxys_list = self.mysql_pool.get_proxys(number)
        return random.choice(proxys_list)

    def update_proxys_fail_count(self, proxy_id):
        self.mysql_pool.update_proxys_fail_count(proxy_id)
        self.mysql_pool.update_proxys_status()

    def acquire_proxy_to_mysql(self, number):
        return False
        url = "http://webapi.http.zhimacangku.com/getip?num=" + str(
            number) + "&type=2&pro=&city=0&yys=0&port=11&pack=106734&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions="
        request = WebRequest.WebRequest()
        r = request.get(url, timeout=10)
        data_list = json.loads(r.content)['data']
        # print(data_list)
        for data in data_list:
            # print(222222)
            # print(data)

            proxy_dict = {
                "proxy": data['ip'] + ":" + str(data['port']),
                "fail_count": 0,
                "region": data['city'],
                "proxy_type": "https",
                "source": "芝麻代理",
                "is_used": 0,
                "expiration_time": data['expire_time'],
                "is_valid": 1,
                "operator": data['isp']
            }
            # print(1111111)
            # print(proxy_dict,222222)
            # print(proxy_dict, 22222222222)
            self.mysql_pool.insert_proxys(**proxy_dict)

    @staticmethod
    def get_proxy_by_free():
        urls = [
            "http://www.xiladaili.com/gaoni/",
        ]
        request = WebRequest.WebRequest()
        ip_list = []
        for url in urls:
            r = request.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "lxml")
            items = soup.select("tbody > tr")
            for item in items:
                ip = item.select_one("td:nth-of-type(1)").get_text()
                protocol_str = item.select_one("td:nth-of-type(2)").get_text()
                if protocol_str.find("https"):
                    protocol = "https"
                else:
                    protocol = "http"
                ip_list.append((ip, protocol))
                # ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", r.text)
                # for ip in ips:
                #     ip_list.append(ip)
                # yield ip.strip()
            # ip_list_all=ip_list
        return random.choice(ip_list)

    def delete_proxy(self, ip_tuple):
        if ip_tuple in self.ip_list:
            self.ip_list.remove(ip_tuple)
        return ip_tuple
    # requests.get("http://39.104.123.45:5010/delete/?proxy={}".format(proxy))
