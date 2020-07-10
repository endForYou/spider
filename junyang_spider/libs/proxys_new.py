"""
@version:1.0
@author: endaqa
@file proxys_new.py
@time 2020/7/10 17:13
"""
import json


class Proxy(object):

    def __init__(self, proxy, fail_count=0, region="", proxy_type="",
                 source="", is_used=0, expiration_time="", is_valid=1, operator=""):
        self._proxy = proxy
        self._fail_count = fail_count  # 默认错误3次代表代理已失效或者被封
        self._region = region  # city
        self._type = proxy_type  # http,https
        self._source = source  # 来源
        self._is_used = is_used  # 是否已经使用
        self._expiration_time = expiration_time
        self._is_valid = is_valid
        self._operator = operator

    @classmethod
    def create_from_json(cls, proxy_json):
        """
        根据proxy属性json创建Proxy实例
        :param proxy_json:
        :return:
        """
        proxy_dict = json.loads(proxy_json)
        return cls(proxy=proxy_dict.get("proxy", ""),
                   fail_count=proxy_dict.get("fail_count", 0),
                   region=proxy_dict.get("region", ""),
                   proxy_type=proxy_dict.get("type", ""),
                   source=proxy_dict.get("source", ""),
                   is_used=proxy_dict.get("is_used", 0),
                   expiration_time=proxy_dict.get("expiration_time", ""),
                   is_valid=proxy_dict.get("is_valid", 0),
                   operator=proxy_dict.get("operator", ""),
                   )

    @property
    def proxy(self):
        """ 代理 ip:port """
        return self._proxy

    @property
    def fail_count(self):
        """ 检测失败次数 """
        return self._fail_count

    @property
    def region(self):
        """ 地理位置(国家/城市) """
        return self._region

    @property
    def type(self):
        """ 透明/匿名/高匿 """
        return self._type

    @property
    def source(self):
        """ 代理来源 """
        return self._source

    @property
    def check_count(self):
        """ 代理检测次数 """
        return self._check_count

    @property
    def last_status(self):
        """ 最后一次检测结果  1 -> 可用; 0 -> 不可用"""
        return self._last_status

    @property
    def last_time(self):
        """ 最后一次检测时间 """
        return self._last_time

    @property
    def to_dict(self):
        """ 属性字典 """
        return {"proxy": self._proxy,
                "fail_count": self._fail_count,
                "region": self._region,
                "type": self._type,
                "source": self._source,
                "check_count": self.check_count,
                "last_status": self.last_status,
                "last_time": self.last_time}

    @property
    def to_json(self):
        """ 属性json格式 """
        return json.dumps(self.to_dict, ensure_ascii=False)

    # --- proxy method ---
    @fail_count.setter
    def fail_count(self, value):
        self._fail_count = value

    @region.setter
    def region(self, value):
        self._region = value

    @type.setter
    def type(self, value):
        self._type = value

    @source.setter
    def source(self, value):
        self._source = value

    @check_count.setter
    def check_count(self, value):
        self._check_count = value

    @last_status.setter
    def last_status(self, value):
        self._last_status = value

    @last_time.setter
    def last_time(self, value):
        self._last_time = value
