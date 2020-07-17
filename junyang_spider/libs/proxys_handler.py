"""
@version:1.0
@author: endaqa
@file proxys_handler.py
@time 2020/7/13 17:24
"""
import json

from junyang_spider.libs.proxys_new import ProxyObj
from junyang_spider.libs.proxys import Proxy
from junyang_spider.libs.redis_client import RedisClient
from junyang_spider.libs import WebRequest
from junyang_spider.libs.mysql_client import MysqlPool


class ProxyHandler(object):
    """ Proxy CRUD operator"""

    def __init__(self, hash_name):

        self.redis_client = RedisClient(hash_name)
        self.mysql_pool = MysqlPool()

    def get(self):
        """
        return a useful proxy
        :return:
        """
        proxy = self.redis_client.get()
        if proxy:
            return ProxyObj.create_from_json(proxy)
        # 如果redis里没有代理，则去请求代理商获取代理
        else:
            data_list = ProxyHandler.acquire_proxy_to_redis()
            for data in data_list:
                proxy = data['ip'] + ":" + str(data['port'])
                fail_count = 0
                region = data['city']
                proxy_type = "https"
                source = "芝麻代理"
                is_used = 0
                expiration_time = data['expire_time']
                is_valid = 1
                operator = data['isp']
                proxys = ProxyObj(proxy, fail_count, region, proxy_type,
                                  source, is_used, expiration_time, is_valid, operator)
                self.put(proxys)

    @staticmethod
    def get_random_proxy():
        return Proxy.get_random_proxy_from_constant_proxys()

    @staticmethod
    def get_proxy_by_free():
        return Proxy.get_proxy_by_free()

    @staticmethod
    def acquire_proxy_to_redis():
        url = "http://webapi.http.zhimacangku.com/getip?num=5&type=2&pro=&city=0&yys=0&port=11&pack=106734&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions="
        request = WebRequest.WebRequest()
        r = request.get(url, timeout=10)
        data_list = json.loads(r.content)
        return data_list


    def get_proxy_from_mysql(self, number):
        sql = "select form proxys where is_valid=1 limit %s" % number
        data_list = self.mysql_pool.fetch_all(sql)

    def pop(self):
        """
        return and delete a useful proxy
        :return:
        """
        proxy = self.redis_client.pop()
        if proxy:
            return ProxyObj.create_from_json(proxy)
        return None

    def put(self, proxy):
        """
        put proxy into use proxy
        :return:
        """
        self.redis_client.put(proxy)

    def delete(self, proxy):
        """
        delete useful proxy
        :param proxy:
        :return:
        """
        return self.redis_client.delete(proxy.proxy)

    def getAll(self):
        """
        get all proxy from pool as Proxy list
        :return:
        """
        proxies_dict = self.redis_client.get_all()
        return [ProxyObj.create_from_json(value) for _, value in proxies_dict.items()]

    def exists(self, proxy):
        """
        check proxy exists
        :param proxy:
        :return:
        """
        return self.redis_client.exists(proxy.proxy)

    def getCount(self):
        """
        return raw_proxy and use_proxy count
        :return:
        """
        total_use_proxy = self.redis_client.getCount()
        return {'count': total_use_proxy}
