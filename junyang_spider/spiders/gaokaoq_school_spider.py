import scrapy
import re
from junyang_spider.items import GkqSchoolItem


class GKQSchoolSpider(scrapy.Spider):
    name = "gaokaoq_school"
    allowed_domains = ["www.gaokaoq.com"]
    start_urls = [
        "http://www.gaokaoq.com/college/lists.html?p=1",

    ]

    def parse(self, response):
        for href in response.css("div.c_name > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)
            # 2,100
        for i in range(2, 172):
            next_url = "http://www.gaokaoq.com/college/lists.html?p=%d" % i
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_dir_contents(self, response):
        school_name = response.css('div.e_name::text').extract_first()
        creation_time_str = response.css('div.attributes tr:nth-child(1)>td:nth-child(1)::text').extract_first().strip()
        creation_time = re.split(r'：', creation_time_str)[1]
        # print(creation_time)

        key_subject_count_str = response.css(
            'div.attributes tr:nth-child(1)>td:nth-child(2)::text').extract_first().strip()
        key_subject_count = re.split(r'：', key_subject_count_str)[1]

        doctor_station_count_str = response.css(
            'div.attributes tr:nth-child(2)>td:nth-child(1)::text').extract_first().strip()
        doctor_station_count = re.split(r'：', doctor_station_count_str)[1]

        master_station_count_str = response.css(
            'div.attributes tr:nth-child(2)>td:nth-child(2)::text').extract_first().strip()
        master_station_count = re.split(r'：', master_station_count_str)[1]

        academician_count_str = response.css(
            'div.attributes tr:nth-child(3)>td:nth-child(2)::text').extract_first().strip()
        academician_count = re.split(r'：', academician_count_str)[1]

        students_count_str = response.css(
            'div.attributes tr:nth-child(4)>td:nth-child(1)::text').extract_first().strip()
        students_count = re.split(r'：', students_count_str)[1]

        national_key_discipline_url = response.urljoin(
            response.css("div.sur_list li:nth-of-type(4) a::attr('href')").extract_first())
        school_desc = response.css('p span::text').extract()
        data_dict = {
            'school_name': school_name,
            'creation_time': creation_time,
            'key_subject_count': key_subject_count,
            'doctor_station_count': doctor_station_count,
            'master_station_count': master_station_count,
            'academician_count': academician_count,
            'students_count': students_count,
            'school_desc': school_desc
        }
        yield scrapy.Request(national_key_discipline_url, meta=data_dict, callback=self.parse_national_key_discipline)

    def parse_national_key_discipline(self, response):
        data_dict = response.meta
        if response.css('td.et1').extract():

            national_key_discipline = response.css('td.et1').extract()
        else:
            national_key_discipline = response.css('p::text').extract()
        data_dict['national_key_discipline'] = national_key_discipline
        parse_feature_specialty_url = response.urljoin(
            response.css("div.s_tabs li:nth-of-type(2) a::attr('href')").extract_first())
        yield scrapy.Request(parse_feature_specialty_url, meta=data_dict, callback=self.parse_feature_specialty)

    def parse_feature_specialty(self, response):
        data_dict = response.meta
        feature_specialty = response.css('p::text').extract()
        data_dict['feature_specialty'] = feature_specialty
        parse_national_key_laboratory_url = response.urljoin(
            response.css("div.s_tabs li:nth-of-type(3) a::attr('href')").extract_first())
        yield scrapy.Request(parse_national_key_laboratory_url, meta=data_dict,
                             callback=self.parse_national_key_laboratory)

    def parse_national_key_laboratory(self, response):
        data_dict = response.meta
        national_key_laboratory = response.css('p::text').extract()
        data_dict['national_key_laboratory'] = national_key_laboratory
        parse_top_discipline_url = response.urljoin(
            response.css("div.s_tabs li:nth-of-type(4) a::attr('href')").extract_first())
        yield scrapy.Request(parse_top_discipline_url, meta=data_dict, callback=self.parse_top_discipline)

    def parse_top_discipline(self, response):
        data_dict = response.meta
        top_discipline = response.css('p::text').extract()
        data_dict['top_discipline'] = top_discipline
        self_enrollment = response.css("li.art a::attr('href')").extract_first()
        if self_enrollment:
            parse_self_enrollment_url = response.urljoin(
                response.css("li.art a::attr('href')").extract_first())
            print(parse_self_enrollment_url)
            yield scrapy.Request(parse_self_enrollment_url, meta=data_dict, callback=self.parse_self_enrollment)
        else:

            item = GkqSchoolItem()
            item['school_name'] = response.meta['school_name']
            item['creation_time'] = response.meta['creation_time']
            item['key_subject_count'] = response.meta['key_subject_count']
            item['students_count'] = response.meta['students_count']
            item['academician_count'] = response.meta['academician_count']
            item['doctor_station_count'] = response.meta['doctor_station_count']
            item['master_station_count'] = response.meta['master_station_count']
            item['school_desc'] = response.meta['school_desc']
            item['national_key_discipline'] = response.meta['national_key_discipline']
            item['feature_specialty'] = response.meta['feature_specialty']
            item['top_discipline'] = response.meta['top_discipline']
            item['national_key_laboratory'] = response.meta['national_key_laboratory']

            yield item

    def parse_self_enrollment(self, response):
        item = GkqSchoolItem()
        item['school_name'] = response.meta['school_name']
        item['creation_time'] = response.meta['creation_time']
        item['key_subject_count'] = response.meta['key_subject_count']
        item['students_count'] = response.meta['students_count']
        item['academician_count'] = response.meta['academician_count']
        item['doctor_station_count'] = response.meta['doctor_station_count']
        item['master_station_count'] = response.meta['master_station_count']
        item['school_desc'] = response.meta['school_desc']
        item['national_key_discipline'] = response.meta['national_key_discipline']
        item['feature_specialty'] = response.meta['feature_specialty']
        item['top_discipline'] = response.meta['top_discipline']
        item['national_key_laboratory'] = response.meta['national_key_laboratory']
        item['self_enrollment'] = response.css('p::text').extract()
        yield item
