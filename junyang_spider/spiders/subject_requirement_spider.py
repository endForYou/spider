"""
@version:1.0
@author: endaqa
@file subject_requirement_spider.py
@time 2019/7/12 17:15
"""
import scrapy
from junyang_spider.items import SubjectRequirementsItem


class SubjectRequirements(scrapy.Spider):
    name = "subject"
    allowed_domains = ["eol.cn", ]
    start_urls = [
        "https://www.eol.cn/e_html/gk/shxk/index.shtml",

    ]
    province_logogram = ["sd", "ah", "bj", "cq", "fj", "gs", "gd", "gx", "gz", "hain", "heb", "hen", "hlj", "hub",
                         "hun", "jl", "js", "jx", "ln", "nmg", "nx", "gh", "sc", "sh", "shx", "sx", "tj", "xg", "xj",
                         "xz", "yn", "zj"]
    need_to_scrapy_province = ["sh", "bj", "zj", "tj", "sd", "hn"]

    def parse(self, response):
        if "pro" in response.meta:
            pro = response.meta['pro']
        else:
            pro = None
        for tr in response.css("tr"):
            requirements_item = SubjectRequirementsItem()
            if tr.css("td:nth-of-type(1)::text").extract_first() == "湖北":
                requirements_item['college_province'] = tr.css("td:nth-of-type(1)::text").extract_first()
                requirements_item['college_name'] = tr.css("td:nth-of-type(2)::text").extract_first()
                requirements_item['grade'] = tr.css("td:nth-of-type(3)::text").extract()
                requirements_item['major_name'] = tr.css("td:nth-of-type(4)::text").extract()
                requirements_item['requirements'] = tr.css("td:nth-of-type(5)::text").extract()
                requirements_item['province'] = pro
            else:
                requirements_item['college_province'] = tr.css("td:nth-of-type(2)::text").extract_first()
                requirements_item['college_name'] = tr.css("td:nth-of-type(3)::text").extract_first()
                requirements_item['grade'] = tr.css("td:nth-of-type(4)::text").extract()
                requirements_item['major_name'] = tr.css("td:nth-of-type(5)::text").extract()
                requirements_item['requirements'] = tr.css("td:nth-of-type(6)::text").extract()
                requirements_item['province'] = pro
            yield requirements_item
        for province in self.need_to_scrapy_province:
            for college_province in self.province_logogram:
                data_dict = {
                    'pro': province}
                url = "https://www.eol.cn/e_html/gk/%sxk/html/html_%s.html" % (province, college_province)
                yield scrapy.Request(url, meta=data_dict, callback=self.parse)
