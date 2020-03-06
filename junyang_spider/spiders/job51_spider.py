# -*- coding: utf-8 -*-
import scrapy
from junyang_spider.items import JunyangSpiderItem


class Job51Spider(scrapy.Spider):
    name = 'job51_spider'
    allowed_domains = ['51job.com']
    place_dic = {
        u"全国": '000000',
        u"长沙": '190200',
    }
    salary_range_dict = {
        u'所有': '99',
        u'2千以下': '01',
        u'2-3千': '02',
        u'3-4.5千': '03',
        u'4.5-6千': '04',
        u'6-8千': '05',
        u'0.8-1万': '06',
        u'1.-1.5万': '07',
        u'1.5-2万': '08',
        u'2-3万': '09',
        u'3-4万': '10',
        u'4-5万': '11',
        u'5万以上': '12',

    }
    education_list = [u'初中', u'高中', u"中专", u'中技', u'大专', u'本科', u'硕士', u'博士']
    release_date_dict = {u'所有': 9, u'24小时内': 0, u'近三天': 1, u'近一周': 2, u'近一月': 3, u'其他': 4}
    key_word_list = ['java', u"软件测试"]
    is_search_all = True
    start_urls = ['https://search.51job.com/list', ]

    def start_requests(self):
        if self.is_search_all:
            self.key_word_list = ["%2B", ]  # 重置关键字列表
        for key_word in self.key_word_list:
            url = self.start_urls[0] + "/%s,000000,0000,00,%d,99,%s,2,1.html" % (self.place_dic[u'全国'],
                                                                                 self.release_date_dict['24小时内'],
                                                                                 key_word)
            data = {
                'lang': 'c',
                'stype': '',
                'postchannel': '0000',
                'workyear': '99',
                'cotype': '99',
                'degreefrom': '99',
                'jobterm': '99',
                'companysize': '99',
                'providesalary': '99',
                'lonlat': '0,0',
                'radius': '-1',
                'ord_field': '0',
                'confirmdate': '0',
                'fromType': '',
                'dibiaoid': '0',
                'address': '',
                'line': '',
                'specialarea': '',
                'from': '',
                'welfare': ''
            }
            meta_data = {
                'key_word': key_word,
            }

            yield scrapy.FormRequest(url, meta=meta_data, formdata=data, method="GET")

    def login(self):
        pass

    def parse(self, response):
        for div in response.css("div.dw_table div.el:nth-of-type(n+4)"):
            item = JunyangSpiderItem()
            item['job_name'] = div.css('p > span > a::text').extract_first()
            source_job_href = div.css('p > span > a::attr("href")').extract_first()
            item['source_job_id'] = source_job_href.split("/")[-1].split(".")[0]
            company_source_company_href = div.css('span.t2 > a::attr("href")').extract_first()
            item['company_source_company_id'] = company_source_company_href.split("/")[-1].split(".")[0]
            item['workplace'] = div.css('span.t3::text').extract_first()
            item['salary'] = div.css('span.t4::text').extract_first()
            item['pubdate'] = div.css('span.t5::text').extract_first()
            url = response.urljoin(source_job_href)
            data_dict = {
                'item': item,
            }
            yield scrapy.Request(url, meta=data_dict, callback=self.parse_job_detail)
        key_word = response.meta['key_word']
        page_count_str = response.css('span.td:nth-of-type(1)::text').extract_first()
        if page_count_str:
            page_count = int(page_count_str[1:3])
            for page in range(2, page_count + 1):
                url = self.start_urls[0] + "/190200,000000,0000,00,%d,99,%s,2,%d.html" % (
                    self.release_date_dict['24小时内'], key_word, page)

                yield scrapy.Request(url, meta=response.meta, callback=self.parse)

    def parse_job_detail(self, response):
        item = response.meta['item']
        item['work_experience_requirement'] = ""
        item['educational_requirements'] = ""
        item['recruiting_numbers'] = ""
        other_requirements_list = []
        for span_text in response.css('div.t1 span::text').extract():
            if span_text.find(u"经验") != -1:
                item['work_experience_requirement'] = span_text
            elif span_text.find(u"招") != -1:
                item['recruiting_numbers'] = span_text
            elif span_text.find(u"发布") != -1:
                continue
            elif span_text in self.education_list:
                item['educational_requirements'] = span_text
            else:
                other_requirements_list.append(span_text)
        item['other_requirements'] = ",".join(other_requirements_list)
        item['benefits'] = response.css("p.t2 span::text").extract()
        item['job_information'] = response.css("div.bmsg.job_msg.inbox").extract_first()

        item['company_name'] = response.css("p.cname a::text").extract_first()
        company_desc = response.css("p.msg::text").extract_first()
        company_desc_list = company_desc.split("|")
        item['company_type'] = company_desc_list[0].strip()
        item['company_staff_number'] = company_desc_list[1].strip()
        item['company_trade'] = company_desc_list[2].strip()
        item['company_contact'] = response.css("div.bmsg > p.fp::text").extract_first()
        item['company_detail_information'] = response.css("div.tmsg").extract_first()
        item['source'] = "51job"
        yield item
