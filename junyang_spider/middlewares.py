# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


# my_proxy = proxys.Proxy()


class JunyangSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JunyangSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # print(22222222222222)
        # proxy_dict = my_proxy.get_proxys_from_mysql(1)
        # # print(proxy_dict,1111111111111)
        # host = proxy_dict['proxy']
        # protocol = "https"
        # # proxy="45.76.114.249:8080"
        # if protocol == "https":
        #     request.meta['proxy'] = "https://{}".format(host)
        # else:
        #     request.meta['proxy'] = "http://{}".format(host)
        # # print(request.meta['proxy'])
        # print(request.headers)
        #
        # self.proxy_id = proxy_dict['id']
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # if response.url.find("denied") != -1 or response.status not in (200, 302, 301):
        #     # delete_proxy(proxy=self.proxy)
        #     # proxy = get_proxy().get("proxy")
        #     my_proxy.update_proxys_fail_count(self.proxy_id)
        #     proxy_dict = my_proxy.get_proxys_from_mysql(1)
        #     host = proxy_dict['proxy']
        #     protocol = "https"
        #     # proxy="45.76.114.249:8080"
        #     if protocol == "https":
        #         request.meta['proxy'] = "https://{}".format(host)
        #     else:
        #         request.meta['proxy'] = "http://{}".format(host)
        #     return request
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        # print(self.proxy_id,111111)
        # print(exception)
        # my_proxy.update_proxys_fail_count(self.proxy_id)
        # proxy_dict = my_proxy.get_proxys_from_mysql(1)
        # host = proxy_dict['proxy']
        # protocol = "https"
        # # proxy="45.76.114.249:8080"
        # if protocol == "https":
        #     request.meta['proxy'] = "https://{}".format(host)
        # else:
        #     request.meta['proxy'] = "http://{}".format(host)
        return request

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JunyangSpiderCustomDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # proxy = my_proxy.get_random_proxy()
        # print(request.headers)
        # proxy = "39.104.97.230:10001"
        # # ip_port = 'secondtransfer.moguproxy.com:9001'
        # # proxy = {"http": "http://" + proxy, }
        # # app_key = 'RHc1bVI4cTBHc1ZodXpkMTpYZ0hlNXlSVG5WRE14NEJV'
        # # proxy_auth = "Basic " + app_key
        # # request.headers["Authorization"] = proxy_auth
        # auth = base64.b64encode(bytes("zhiya:kw303LL9", 'utf-8'))
        # request.headers['Proxy-Authorization'] = b'Basic ' + auth
        #
        # request.meta['proxy'] = "http://{}".format(proxy)
        # print(request.meta['proxy'])
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # print(response.headers)
        # print(response.text)
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # if response.url.find("denied") != -1 or response.status not in (200, 302):
        #     # delete_proxy(proxy=self.proxy)
        #     # proxy = get_proxy().get("proxy")
        #     my_proxy.delete_proxy(self.proxy)
        #     proxy_tuple = random.choice(my_proxy.get_proxy())
        #     ip = proxy_tuple[0]
        #     protocol = proxy_tuple[1]
        #     # proxy="45.76.114.249:8080"
        #     if protocol == "https":
        #         request.meta['proxy'] = "https://{}".format(ip)
        #     else:
        #         request.meta['proxy'] = "http://{}".format(ip)
        #     return request
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JunyangSpiderFixedDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # proxy = my_proxy.get_random_proxy_from_constant_proxys()
        # request.meta['proxy'] = "http://{}".format(proxy)
        # # print(request.meta['proxy'])
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # if response.url.find("denied") != -1 or response.status not in (200, 302):
        #     # delete_proxy(proxy=self.proxy)
        #     # proxy = get_proxy().get("proxy")
        #     my_proxy.delete_proxy(self.proxy)
        #     proxy_tuple = random.choice(my_proxy.get_proxy())
        #     ip = proxy_tuple[0]
        #     protocol = proxy_tuple[1]
        #     # proxy="45.76.114.249:8080"
        #     if protocol == "https":
        #         request.meta['proxy'] = "https://{}".format(ip)
        #     else:
        #         request.meta['proxy'] = "http://{}".format(ip)
        #     return request
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
