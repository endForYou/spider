"""
@version:1.0
@author: endaqa
@file yzy.py
@time 2019/11/20 17:09
"""
# coding=utf-8
import os

import json
import ctypes

# django.setup()

import requests
import re
# from etiaky.models import RecruitZhpjPython
# from etiaky.report import report_base
import sys

# import urllib
from urllib.parse import quote


def show_number(numbers):
    pattern = re.compile(r'[g-t]')
    old = ""
    number = ""  # var number = "";
    for values in numbers.split("|"):  # myNumbers.split("|").forEach(function(value)
        value = re.sub(pattern, old, values)  # value = value.replace(/[g-t]/ig,"");
        number += "&#x" + value + ";"  # number += "&#x" + value + ";"
    num_mappings = FontTransfer.get_num_mappings()
    result = ""
    for i in number.split(";")[0:-1]:
        # print(i)
        if i in num_mappings.keys():
            v = num_mappings[i]
        else:
            v = i
        result += v
    return result


def show_str(data):
    yb2 = ""
    data_list = data.split("|")
    for v in data_list:
        if re.search("【(.*?)】", v):
            yb2 += v.replace("【", "").replace("】", "") + ";"
        else:
            v = re.sub("[g-t]", "", v)

            yb2 += "&#x" + v + ";"
    #print(yb2)
    str_mappings = FontTransfer.get_str_mappings()
    result = ""
    for i in yb2.split(";")[0:-1]:
        # print(i)
        if i in str_mappings.keys():
            v = str_mappings[i]
        else:
            v = i
        result += v
    return result


class FontTransfer:
    @staticmethod
    def get_str_mappings():
        # '&#xb538': '历'
        # &#xb8c 磁
        # &#xb8c1
        str_mappings = {'&#xb0cf': '像', '&#xb27a': '艺', '&#xb305': '包',
                        '&#xb36e': '据', '&#xb370': '印', '&#xb3a2': '探', '&#xb3ca': '及', '&#xb425': '营', '&#xb47d': '命',
                        '&#xb5386': '历', '&#xb6f2': '曲', '&#xb70d': '服', '&#xb73a': '机', '&#xb883': '境', '&#xb8b0': '械',
                        '&#xb8c': '磁', '&#xb8de': '飞', '&#xb8df': '食', '&#xb907': '备', '&#xb90d': '植', '&#xba7a': '空',
                        '&#xbb66': '武', '&#xbbbe': '设', '&#xbc34': '水', '&#xbc45': '居', '&#xbcb9': '油', '&#xbd0b': '洋',
                        '&#xbd4b': '测', '&#xbebd': '钮', '&#xbedf': '统', '&#xbef6': '件', '&#xbf6f': '软', '&#xbf7b': '轻',
                        '&#xbf8e': '美', '&#xc620': '丁', '&#xc621': '下', '&#xc622': '与', '&#xc623': '世', '&#xc624': '业',
                        '&#xc625': '丝', '&#xc626': '中', '&#xc627': '主', '&#xc628': '义', '&#xc629': '乌', '&#xc62a': '书',
                        '&#xc62b': '事', '&#xc62c': '互', '&#xc62d': '交', '&#xc62e': '产', '&#xc62f': '人', '&#xc630': '仪',
                        '&#xc631': '价', '&#xc632': '休', '&#xc633': '会', '&#xc634': '伤', '&#xc635': '伦', '&#xc636': '估',
                        '&#xc637': '体', '&#xc638': '作', '&#xc639': '供', '&#xc63a': '侦', '&#xc63b': '俄', '&#xc63c': '保',
                        '&#xc63d': '信', '&#xc63e': '修', '&#xc63f': '健', '&#xc640': '儿', '&#xc641': '光', '&#xc642': '克',
                        '&#xc643': '党', '&#xc644': '全', '&#xc645': '公', '&#xc646': '共', '&#xc647': '关', '&#xc648': '兵',
                        '&#xc649': '其', '&#xc64a': '军', '&#xc64b': '农', '&#xc64c': '准', '&#xc64d': '减', '&#xc64e': '出',
                        '&#xc64f': '分', '&#xc650': '划', '&#xc651': '则', '&#xc652': '别', '&#xc653': '制', '&#xc654': '刷',
                        '&#xc655': '力', '&#xc656': '功', '&#xc657': '加', '&#xc658': '务', '&#xc659': '动', '&#xc65a': '助',
                        '&#xc65b': '劳', '&#xc65c': '化', '&#xc65d': '医', '&#xc65e': '华', '&#xc65f': '卫', '&#xc660': '发',
                        '&#xc661': '古', '&#xc662': '史', '&#xc663': '司', '&#xc664': '合', '&#xc665': '告', '&#xc666': '品',
                        '&#xc667': '商', '&#xc668': '回', '&#xc669': '国', '&#xc66a': '土', '&#xc66b': '地', '&#xc66c': '型',
                        '&#xc66d': '培', '&#xc66e': '声', '&#xc66f': '大', '&#xc670': '天', '&#xc671': '女', '&#xc672': '媒',
                        '&#xc673': '子', '&#xc674': '学', '&#xc675': '安', '&#xc676': '定', '&#xc677': '宝', '&#xc678': '实',
                        '&#xc679': '审', '&#xc67a': '室', '&#xc67b': '家', '&#xc67c': '宾', '&#xc67d': '密', '&#xc67e': '小',
                        '&#xc67f': '少', '&#xc680': '尔', '&#xc681': '展', '&#xc682': '属', '&#xc683': '嵌', '&#xc684': '工',
                        '&#xc685': '市', '&#xc686': '师', '&#xc687': '广', '&#xc688': '应', '&#xc689': '康', '&#xc68a': '建',
                        '&#xc68b': '开', '&#xc68c': '录', '&#xc68d': '形', '&#xc68e': '影', '&#xc68f': '律', '&#xc690': '微',
                        '&#xc691': '德', '&#xc692': '心', '&#xc693': '情', '&#xc694': '想', '&#xc695': '感', '&#xc696': '成',
                        '&#xc697': '战', '&#xc698': '房', '&#xc699': '技', '&#xc69a': '投', '&#xc69b': '护', '&#xc69c': '报',
                        '&#xc69d': '拉', '&#xc69e': '控', '&#xc69f': '推', '&#xc6a0': '播', '&#xc6a1': '收', '&#xc6a2': '放',
                        '&#xc6a3': '政', '&#xc6a4': '教', '&#xc6a5': '数', '&#xc6a6': '文', '&#xc6a7': '料', '&#xc6a8': '斯',
                        '&#xc6a9': '无', '&#xc6aa': '日', '&#xc6ab': '时', '&#xc6ac': '景', '&#xc6ad': '智', '&#xc6ae': '术',
                        '&#xc6af': '材', '&#xc6b0': '村', '&#xc6b1': '来', '&#xc6b2': '查', '&#xc6b3': '正', '&#xc6b4': '民',
                        '&#xc6b5': '气', '&#xc6b6': '污', '&#xc6b7': '河', '&#xc6b8': '治', '&#xc6b9': '法', '&#xc6ba': '泰',
                        '&#xc6bb': '海', '&#xc6bc': '源', '&#xc6bd': '灾', '&#xc6be': '炸', '&#xc6bf': '然', '&#xc6c0': '照',
                        '&#xc6c1': '爆', '&#xc6c2': '版', '&#xc6c3': '物', '&#xc6c4': '环', '&#xc6c5': '班', '&#xc6c6': '理',
                        '&#xc6c7': '生', '&#xc6c8': '用', '&#xc6c9': '画', '&#xc6ca': '界', '&#xc6cb': '疗', '&#xc6cc': '监',
                        '&#xc6cd': '知', '&#xc6ce': '石', '&#xc6cf': '研', '&#xc6d0': '种', '&#xc6d1': '科', '&#xc6d2': '秘',
                        '&#xc6d3': '移', '&#xc6d4': '程', '&#xc6d5': '税', '&#xc6d6': '立', '&#xc6d7': '筑', '&#xc6d8': '算',
                        '&#xc6d9': '管', '&#xc6da': '类', '&#xc6db': '精', '&#xc6dc': '纺', '&#xc6dd': '组', '&#xc6de': '织',
                        '&#xc6df': '经', '&#xc6e0': '网', '&#xc6e1': '职', '&#xc6e2': '育', '&#xc6e3': '能', '&#xc6e4': '自',
                        '&#xc6e5': '航', '&#xc6e6': '船', '&#xc6e7': '英', '&#xc6e8': '草', '&#xc6e9': '萄', '&#xc6ea': '葡',
                        '&#xc6eb': '行', '&#xc6ec': '表', '&#xc6ed': '装', '&#xc6ee': '观', '&#xc6ef': '规', '&#xc6f0': '视',
                        '&#xc6f1': '计', '&#xc6f2': '论', '&#xc6f3': '评', '&#xc6f4': '识', '&#xc6f5': '译', '&#xc6f6': '试',
                        '&#xc6f7': '语', '&#xc6f8': '财', '&#xc6f9': '质', '&#xc6fa': '资', '&#xc6fb': '路', '&#xc6fc': '车',
                        '&#xc6fd': '轨', '&#xc6fe': '轮', '&#xc6ff': '运', '&#xc700': '通', '&#xc701': '造', '&#xc702': '采',
                        '&#xc703': '量', '&#xc704': '金', '&#xc705': '鉴', '&#xc706': '间', '&#xc707': '非', '&#xc708': '韩',
                        '&#xc709': '项', '&#xc70a': '预', '&#xc70b': '饰', '&#xc70c': '馆', '&#xc70d': '验', '&#xc70e': '高',
                        '&#xc70f': '麻', '&#xc710': '（', '&#xc711': '）', '&#xc3a': '0', '&#xc30': '1', '&#xc33': '2',
                        '&#xc3b': '3', '&#xc31': '4', '&#xc34': '5', '&#xc3c': '6', '&#xc32': '7', '&#xc35': '8',
                        '&#xc3d': '9', '&#xc411': 'A', '&#xc421': 'B', '&#xc431': 'C', '&#xc441': 'D', '&#xc451': 'E',
                        '&#xc461': 'F', '&#xc471': 'G', '&#xc481': 'H', '&#xc491': 'I', '&#xc4a1': 'J', '&#xc4b1': 'K',
                        '&#xc4c1': 'L', '&#xc4d1': 'M', '&#xc4e1': 'N', '&#xc4f1': 'O', '&#xc501': 'P', '&#xc511': 'Q',
                        '&#xc521': 'R', '&#xc531': 'S', '&#xc541': 'T', '&#xc551': 'U', '&#xc561': 'V', '&#xc571': 'W',
                        '&#xc581': 'X', '&#xc591': 'Y', '&#xc5a1': 'Z', '&#xc736': 'a', '&#xc737': 'b', '&#xc738': 'c',
                        '&#xc739': 'd', '&#xc73a': 'e', '&#xc73b': 'f', '&#xc73c': 'g', '&#xc73d': 'h', '&#xc73e': 'i',
                        '&#xc73f': 'j', '&#xc740': 'k', '&#xc741': 'l', '&#xc742': 'm', '&#xc743': 'n', '&#xc744': 'o',
                        '&#xc745': 'p', '&#xc746': 'q', '&#xc747': 'r', '&#xc748': 's', '&#xc749': 't', '&#xc74a': 'u',
                        '&#xc74b': 'v', '&#xc74c': 'w', '&#xc74d': 'x', '&#xc74e': 'y', '&#xc74f': 'z', "&#x": ''}

        # print(len(str_mappings))
        # result={}
        # for k, v in str_mappings.items():
        #     if v not in result.keys():
        #         result[v]=1
        #     else:
        #         result[v]=2
        # print(result)

        return str_mappings

    @staticmethod
    def get_num_mappings():
        num_mappings = {
            '&#xa8f2e': '0', '&#xc15f9': '1', '&#x7d3ae': '2',
            '&#xf8b41': '3', '&#xc2e7a': '4', '&#xe7f11': '5', '&#x6f732': '6', '&#xaa86e': '7', '&#xfc6a6': '8',
            '&#x72ef1': '9', "&#x": ""
        }
        return num_mappings


if __name__ == '__main__':
    FontTransfer.get_str_mappings()
    pass
