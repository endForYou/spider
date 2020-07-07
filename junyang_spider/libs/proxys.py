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


class Proxy:
    def __init__(self):
        self.ip_list = []

    def get_random_proxy(self):
        ip_list = [
            "1.196.116.90:40916", "60.172.83.221:28803", "60.189.126.131:31665", "117.69.244.142:28803",
            "125.120.200.133:27986", "222.133.167.188:13504",
            "119.132.68.38:28803", "221.203.128.243:28469"
        ]
        return random.choice(ip_list)

    def get_proxy(self):
        if not self.ip_list:
            urls = [
                # 'http://www.xiladaili.com/putong/',
                "http://webapi.http.zhimacangku.com/getip?num=3&type=2&pro=&city=0&yys=0&port=11&pack=106734&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions=",
                # "https://proxyapi.horocn.com/api/v2/proxies?order_id=YQMR1671088109301290&num=10&format=json&line_separator=win&can_repeat=no&user_token=10212378e50acf6233804e2fe6851af4",
                # "http://www.xiladaili.com/https/"
            ]
            request = WebRequest.WebRequest()
            ip_list = []
            for url in urls:
                r = request.get(url, timeout=10)
                data = json.loads(r.content)
                for item in data['data']:
                    ip = item['ip']
                    #ip = item['host']
                    port = item['port']
                    ip_list.append((ip + ":" + str(port), "https"))
                    # print(ip_list)
                # ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", r.text)
                # for ip in ips:
                #     ip_list.append(ip)
                # yield ip.strip()
            # ip_list_all=ip_list

            self.ip_list = ip_list
        return self.ip_list

    def get_proxy_by_free(self):
        if not self.ip_list:
            urls = [
                # 'http://www.xiladaili.com/putong/',
                "http://www.xiladaili.com/gaoni/",
                # "http://www.xiladaili.com/http/",
                # "http://www.xiladaili.com/https/"
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
            self.ip_list = ip_list
        return self.ip_list

    def delete_proxy(self, ip_tuple):
        if ip_tuple in self.ip_list:
            self.ip_list.remove(ip_tuple)
        return ip_tuple
        # requests.get("http://39.104.123.45:5010/delete/?proxy={}".format(proxy))
