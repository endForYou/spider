"""
@version:1.0
@author: endaqa
@file redis_client.py
@time 2020/7/3 11:37
"""
from redis.connection import BlockingConnectionPool
from random import choice
from redis import Redis
from junyang_spider.libs.singleton import Singleton


class RedisClient(object):
    __metaclass__ = Singleton
    """
    Redis client
    Redis中代理存放的结构为hash：
    key为ip:port, value为代理属性的字典;
    """

    def __init__(self, hash_name, **kwargs):
        """
        init
        :param host: host
        :param port: port
        :param password: password
        :param db: db
        :return:
        """
        self.name = hash_name
        kwargs.pop("username")
        self.__conn = Redis(connection_pool=BlockingConnectionPool(decode_responses=True, **kwargs))

    def get(self):
        """
        返回一个代理
        :return:
        """
        proxies = self.__conn.hkeys(self.name)
        proxy = choice(proxies) if proxies else None
        if proxy:
            return self.__conn.hget(self.name, proxy)
        else:
            return False

    def put(self, proxy_obj):
        """
        将代理放入hash, 使用changeTable指定hash name
        :param proxy_obj: Proxy obj
        :return:
        """
        data = self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.to_json)
        return data

    def pop(self):
        """
        弹出一个代理
        :return: dict {proxy: value}
        """
        proxies = self.__conn.hkeys(self.name)
        for proxy in proxies:
            proxy_info = self.__conn.hget(self.name, proxy)
            self.__conn.hdel(self.name, proxy)
            return proxy_info
        else:
            return False

    def delete(self, proxy_str):
        """
        移除指定代理, 使用changeTable指定hash name
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hdel(self.name, proxy_str)

    def exists(self, proxy_str):
        """
        判断指定代理是否存在, 使用changeTable指定hash name
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hexists(self.name, proxy_str)

    def update(self, proxy_obj):
        """
        更新 proxy 属性
        :param proxy_obj:
        :return:
        """
        return self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.to_json)

    def get_all(self):
        """
        字典形式返回所有代理, 使用change_table指定hash name
        :return:
        """
        item_dict = self.__conn.hgetall(self.name)
        return item_dict

    def clear(self):
        """
        清空所有代理, 使用changeTable指定hash name
        :return:
        """
        return self.__conn.delete(self.name)

    def getCount(self):
        """
        返回代理数量
        :return:
        """
        return self.__conn.hlen(self.name)

    def change_table(self, name):
        """
        切换操作对象
        :param name:
        :return:
        """
        self.name = name
