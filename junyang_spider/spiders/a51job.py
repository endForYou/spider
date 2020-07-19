# """
# @version:1.0
# @author: endaqa
# @file a51job.py
# @time 2019/8/21 15:22
# """
# # -*- coding: utf-8 -*-
# import json, pymysql
# import re
#
# from scrapy import Spider, Request, Selector, signals
# from junyang_spider.items import FoJobItem
# #from scrapy.conf import settings
#
#
# # from scrapy_redis.spiders import RedisSpider
#
#
# class A51jobSpider(Spider):
#     name = 'a51job'
#     allowed_domains = ['51job.com']
#
#     def __init__(self, **kwargs):
#         super().__init__(name=None, **kwargs)
#
#         self.connect = pymysql.connect(
#             host=settings.get('MYSQL_HOST'),
#             port=settings.get('MYSQL_PORT'),
#             db=settings.get('MYSQL_DBNAME'),
#             user=settings.get('MYSQL_USER'),
#             passwd=settings.get('MYSQL_PASSWD'),
#             charset='utf8',
#             use_unicode=True)
#         self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
#
#     base_url = 'https://search.51job.com/list/{location},000000,{function},{industry},9,99,%2520,2,{page}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
#     count = 0
#
#     def start_requests(self):
#         self.cursor.execute('select * from region where code%10000=0')
#         regions = self.cursor.fetchall()
#         self.cursor.execute('select * from `function` where code%100=0')
#         functions = self.cursor.fetchall()
#         for region in regions:
#             for func in functions:
#                 yield Request(
#                     self.base_url.format(location=region['code'], industry='00', function=func['code'], page=1),
#                     meta={"region": region, 'function': func}, callback=self.parse, dont_filter=True)
#                 break
#             break
#
#     def parse(self, response):
#         regions = response.request.meta['region']
#         functions = response.request.meta['function']
#         count = int(response.xpath('normalize-space(//div[@class="dw_tlc"]/div[4]/text())').re_first('\d+'))
#         print(f'province:{regions}', f"function:{functions}", f"count is :{count}")
#         if count >= 100000:
#             rcode = regions.get('code')
#             fcode = functions.get('code')
#             if int(fcode) % 100 != 0:  # 子职能超过10W, 把省分为城市查询
#                 self.cursor.execute(f"select * from region where code like '{rcode[:2]}%' and code!={rcode}")
#                 for region in self.cursor.fetchall():
#                     yield Request(
#                         self.base_url.format(location=region.get('code'), industry='00', function=fcode, page=1),
#                         meta={"region": region, 'function': response.meta['function']}, callback=self.parse,
#                         dont_filter=True)
#             else:
#                 self.cursor.execute(f"select * from function where code like '{fcode[:2]}%' and code!={fcode}")
#
#                 # print(self.cursor.fetchall())
#                 for func in self.cursor.fetchall():
#                     yield Request(self.base_url.format(location=response.meta["region"]['code'], industry='00',
#                                                        function=func.get('code'), page=1),
#                                   meta={"region": response.meta["region"], 'function': func},
#                                   callback=self.parse, dont_filter=True)
#         else:
#             self.count += count
#             print(f'current count is : {self.count}')
#             page_count = int(response.css('.dw_page span.td:first-of-type::text').re_first('\d+'))
#             for pageNum in range(1, page_count + 1):
#                 yield Request(self.base_url.format(location=regions['code'], industry='00',
#                                                    function=functions['code'], page=pageNum),
#                               meta={"region": regions, 'function': functions}, callback=self.parse_paging, priority=100,
#                               dont_filter=True)
#
#     def parse_paging(self, response):
#         _headers = {
#             "Host": "jobs.51job.com",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "none",
#             "Sec-Fetch-User": "?1",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
#         }
#         regions = response.request.meta['region']
#         functions = response.request.meta['function']
#         for url in response.css('.el > p a::attr(href)').extract():
#             yield Request(url, meta={"region": regions, 'function': functions}, callback=self.parse_resume,
#                           priority=200, dont_filter=True,headers=_headers)
#
#     def parse_resume(self, response):
#         # print(response.request.meta['region'])
#         item = FoJobItem()
#         item['Id'] = response.css('#hidJobID::attr(value)').extract_first()
#         item['Rid'] = response.request.meta['region']['id']
#         item['Fid'] = response.request.meta['function']['id']
#         item['JobUrl'] = response.request.url
#         item['JobTitle'] = response.xpath('//div[contains(@class,"tHeader")]//h1/@title').extract_first()
#         item['CompanyName'] = response.css('.cname a::text').extract_first()
#         item['SalaryRange'] = response.css('.tHeader .cn strong::text').extract_first()
#         item['RequireInfo'] = response.xpath(
#             'translate(normalize-space(string(//p[@class="msg ltype"])),"\xa0","")').extract_first()
#
#         if item['CompanyName']:
#             item['CompanyName'] = item['CompanyName'].strip()
#         item['CompanyBenefits'] = ','.join(response.css('.jtag span.sp4::text').extract())  # 公司福利
#         # if item['CompanyBenefits'] == '': item['CompanyBenefits'] = None
#         item['CompanyType'] = response.xpath(
#             '//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p[1]/text()').extract_first()
#         item['CompanyPeople'] = response.xpath(
#             '//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p[2]/text()').extract_first()
#         item['CompanyIndustry'] = response.xpath(
#             'normalize-space(//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p[3]/@title)').extract_first()
#
#         item['JobInfo'] = Selector(text=re.search(
#             '<div class="tBorderTop_box">.*?职位信息.*?<div class="bmsg job_msg inbox">(.*?)<div class="mt10">',
#             response.text, re.S).group(1)).xpath('translate(normalize-space(.),"\xa0","")').extract_first()
#         item['Functions'] = response.xpath(
#             'normalize-space(string(//div[@class="mt10"]/p[@class="fp"][1]))').extract_first()
#         item['KeyWords'] = response.xpath(
#             'normalize-space(string(//div[@class="mt10"]/p[@class="fp"][2]))').extract_first()
#         # if item['KeyWords'] == '': item['KeyWords'] = None
#         item['CompanyDepart'] = response.xpath(
#             "//div[@class='tCompany_main']/div[@class='tBorderTop_box']//span[@class='bname' and text()='部门信息']/parent::h2/following-sibling::div/text()").extract()
#         if len(item['CompanyDepart']) >= 2:
#             item['CompanyDepart'] = item['CompanyDepart'][1].strip()
#         else:
#             item['CompanyDepart'] = ''
#         item['CompanyAddress'] = response.xpath(
#             "//div[@class='tCompany_main']/div[@class='tBorderTop_box']//span[@class='bname' and text()='联系方式']/parent::h2/following-sibling::div/p/text()").extract()
#
#         if len(item['CompanyAddress']) >= 2:
#             item['CompanyAddress'] = item['CompanyAddress'][1].strip()
#         else:
#             item['CompanyAddress'] = ''
#         item['CompanyProfile'] = ''.join([text.strip() for text in response.xpath(
#             "//div[@class='tCompany_main']/div[@class='tBorderTop_box']//span[@class='bname' and text()='公司信息']/parent::h2/following-sibling::div/text()").extract()]).replace(
#             '\xa0', '').replace('\t', '')
#         return item
