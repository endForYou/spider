import requests
import json
import urllib3
from apscheduler.schedulers.blocking import BlockingScheduler

from junyang_spider.libs.mail import Mail
from apscheduler.jobstores.redis import *

urllib3.disable_warnings()
mail = Mail()


class ServiceMonitor:

    def __init__(self):
        self._token = "Bearer "
        self._enterprise_token = "Bearer "

    # login
    def user_login(self):
        payload = {
            "phoneNumber": "19999900001",
            "password": "jy123456",
            "clientType": "PC"
        }
        headers = {
            "Content-Type": "application/json",
        }
        try:
            res = requests.post("https://wechat.junyanginfo.com/login/byPassword", headers=headers,
                                data=json.dumps(payload))
            token = res.json()['token']
            self._token += token
            return True
        except BaseException as e:
            return False

    # user
    def update_user_province_ogk(self):
        payload = {"id": 47673, "phoneNumber": "19999900001", "province": {"id": 530000}, "city": {"id": 530100},
                   "district": {"id": 530122}, "isValid": True, "isSuperUser": True, "wechatOpenId": None,
                   "school": {"id": 2050}, "gender": True, "startYear": "高一", "level": "XUE_XI", "userId": 53994,
                   "name": "知涯", "nickName": None,
                   "image": "file:///storage/emulated/0/Android/data/com.zhiyaxuanke.zysxapp/files/Pictures/94b93d0a-f471-4aa3-8647-31cd73269290.jpg",
                   "startDate": 1648800930000, "endDate": None, "userIdentity": 1, "scienceArt": "理科", "position": 3928,
                   "code": 1, "modifyTimes": 0, "score": 550, "evaluationId": 4853, "hintState": 0, "className": "1",
                   "createdDateTime": 1583135857993,
                   "authorities": ["YUANXIAO", "ZHIYE", "SHENGYA", "XUANKE", "CEPING", "ZHIYUAN", "TIKU", "ZHUANYE",
                                   "K12"],
                   "validRoles": [{"name": "ZHI_YUAN", "startDateTime": 1648799956000, "endDateTime": 1680335956000},
                                  {"name": "XUE_XI", "startDateTime": 1648800930000, "endDateTime": 1680336930000},
                                  {"name": "SHENG_XUE", "startDateTime": 1585037344000, "endDateTime": 2089958944000}],
                   "roles": [{"id": 97310, "role": {"id": 2, "name": "XUAN_KE", "description": "选科VIP角色",
                                                    "authorities": [{"id": 5, "name": "CEPING"},
                                                                    {"id": 9, "name": "ZHIYE"},
                                                                    {"id": 1, "name": "SHENGYA"},
                                                                    {"id": 7, "name": "YUANXIAO"},
                                                                    {"id": 3, "name": "XUANKE"},
                                                                    {"id": 6, "name": "TIKU"}], "level": "XUAN_KE"},
                              "startDateTime": 1650954660000, "endDateTime": 1655274660000, "level": "XUAN_KE"},
                             {"id": 97018, "role": {"id": 7, "name": "XUE_XI", "description": "学习VIP角色",
                                                    "authorities": [{"id": 1, "name": "SHENGYA"},
                                                                    {"id": 3, "name": "XUANKE"},
                                                                    {"id": 2, "name": "K12"},
                                                                    {"id": 6, "name": "TIKU"}], "level": "XUE_XI"},
                              "startDateTime": 1648800930000, "endDateTime": 1680336930000, "level": "XUE_XI"},
                             {"id": 49557, "role": {"id": 5, "name": "SHENG_XUE", "description": "升学VIP角色(超级VIP)",
                                                    "authorities": [{"id": 5, "name": "CEPING"},
                                                                    {"id": 4, "name": "ZHIYUAN"},
                                                                    {"id": 9, "name": "ZHIYE"},
                                                                    {"id": 1, "name": "SHENGYA"},
                                                                    {"id": 7, "name": "YUANXIAO"},
                                                                    {"id": 3, "name": "XUANKE"},
                                                                    {"id": 2, "name": "K12"},
                                                                    {"id": 8, "name": "ZHUANYE"},
                                                                    {"id": 6, "name": "TIKU"}], "level": "SHENG_XUE"},
                              "startDateTime": 1585037344000, "endDateTime": 2089958944000, "level": "SHENG_XUE"},
                             {"id": 99835, "role": {"id": 1, "name": "ZHI_YUAN", "description": "志愿VIP角色",
                                                    "authorities": [{"id": 5, "name": "CEPING"},
                                                                    {"id": 4, "name": "ZHIYUAN"},
                                                                    {"id": 9, "name": "ZHIYE"},
                                                                    {"id": 1, "name": "SHENGYA"},
                                                                    {"id": 7, "name": "YUANXIAO"},
                                                                    {"id": 3, "name": "XUANKE"},
                                                                    {"id": 2, "name": "K12"},
                                                                    {"id": 8, "name": "ZHUANYE"},
                                                                    {"id": 6, "name": "TIKU"}], "level": "ZHI_YUAN"},
                              "startDateTime": 1650954660000, "endDateTime": 1655274660000, "level": "ZHI_YUAN"},
                             {"id": 96995, "role": {"id": 1, "name": "ZHI_YUAN", "description": "志愿VIP角色",
                                                    "authorities": [{"id": 5, "name": "CEPING"},
                                                                    {"id": 4, "name": "ZHIYUAN"},
                                                                    {"id": 9, "name": "ZHIYE"},
                                                                    {"id": 1, "name": "SHENGYA"},
                                                                    {"id": 7, "name": "YUANXIAO"},
                                                                    {"id": 3, "name": "XUANKE"},
                                                                    {"id": 2, "name": "K12"},
                                                                    {"id": 8, "name": "ZHUANYE"},
                                                                    {"id": 6, "name": "TIKU"}], "level": "ZHI_YUAN"},
                              "startDateTime": 1648799956000, "endDateTime": 1680335956000, "level": "ZHI_YUAN"}],
                   "gotoZhiyuanPage": False,
                   "subjects": [{"id": 1, "name": "物理"}, {"id": 2, "name": "化学"}, {"id": 3, "name": "生物"}],
                   "enrollBatchId": 1024, "platformId": None, "scienceAndArt": "理科"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }

        try:
            res = requests.post("https://wechat.junyanginfo.com/user/users/updateUser", headers=headers,
                                data=json.dumps(payload), verify=False)
            if res.status_code != 200:
                return "zhiyuan-更新用户老高考省份失败，请检查服务"
            province = res.json()['province']['id']
            if province != 530000:
                return "zhiyuan-更新用户老高考省份失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "zhiyuan-更新用户老高考省份失败，请检查服务"

    def update_user_province_ngk(self):
        payload = {"id": 47673, "phoneNumber": "19999900001", "province": {"id": 430000}, "city": {"id": 430200},
                   "district": {"id": 430203}, "isValid": True, "isSuperUser": True, "wechatOpenId": None,
                   "school": {"id": 8187}, "gender": True, "startYear": "高一", "level": "XUE_XI", "userId": 53994,
                   "name": "知涯", "nickName": None,
                   "image": "file:///storage/emulated/0/Android/data/com.zhiyaxuanke.zysxapp/files/Pictures/94b93d0a-f471-4aa3-8647-31cd73269290.jpg",
                   "startDate": 1648800930000, "endDate": None, "userIdentity": 1, "scienceArt": "理科",
                   "position": 39282, "code": 1, "modifyTimes": 0, "score": 550, "evaluationId": 4853, "hintState": 0,
                   "className": "1", "createdDateTime": 1583135857993,
                   "authorities": ["YUANXIAO", "ZHIYE", "SHENGYA", "XUANKE", "CEPING", "ZHIYUAN", "TIKU", "ZHUANYE",
                                   "K12"],
                   "validRoles": [{"name": "ZHI_YUAN", "startDateTime": 1648799956000, "endDateTime": 1680335956000},
                                  {"name": "XUE_XI", "startDateTime": 1648800930000, "endDateTime": 1680336930000},
                                  {"name": "SHENG_XUE", "startDateTime": 1585037344000, "endDateTime": 2089958944000}],
                   "roles": [{"id": 97310, "role": {"id": 2, "name": "XUAN_KE", "description": "选科VIP角色",
                                                    "authorities": [{"id": 5, "name": "CEPING"},
                                                                    {"id": 9, "name": "ZHIYE"},
                                                                    {"id": 1, "name": "SHENGYA"},
                                                                    {"id": 7, "name": "YUANXIAO"},
                                                                    {"id": 3, "name": "XUANKE"},
                                                                    {"id": 6, "name": "TIKU"}], "level": "XUAN_KE"},
                              "startDateTime": 1650954660000, "endDateTime": 1655274660000, "level": "XUAN_KE"},
                             {"id": 97018, "role": {"id": 7, "name": "XUE_XI", "description": "学习VIP角色",
                                                    "authorities": [{"id": 1, "name": "SHENGYA"},
                                                                    {"id": 3, "name": "XUANKE"},
                                                                    {"id": 2, "name": "K12"},
                                                                    {"id": 6, "name": "TIKU"}], "level": "XUE_XI"},
                              "startDateTime": 1648800930000, "endDateTime": 1680336930000, "level": "XUE_XI"},
                             {"id": 49557, "role": {"id": 5, "name": "SHENG_XUE", "description": "升学VIP角色(超级VIP)",
                                                    "authorities": [{"id": 5, "name": "CEPING"},
                                                                    {"id": 4, "name": "ZHIYUAN"},
                                                                    {"id": 9, "name": "ZHIYE"},
                                                                    {"id": 1, "name": "SHENGYA"},
                                                                    {"id": 7, "name": "YUANXIAO"},
                                                                    {"id": 3, "name": "XUANKE"},
                                                                    {"id": 2, "name": "K12"},
                                                                    {"id": 8, "name": "ZHUANYE"},
                                                                    {"id": 6, "name": "TIKU"}], "level": "SHENG_XUE"},
                              "startDateTime": 1585037344000, "endDateTime": 2089958944000, "level": "SHENG_XUE"},
                             {"id": 99835, "role": {"id": 1, "name": "ZHI_YUAN", "description": "志愿VIP角色",
                                                    "authorities": [{"id": 5, "name": "CEPING"},
                                                                    {"id": 4, "name": "ZHIYUAN"},
                                                                    {"id": 9, "name": "ZHIYE"},
                                                                    {"id": 1, "name": "SHENGYA"},
                                                                    {"id": 7, "name": "YUANXIAO"},
                                                                    {"id": 3, "name": "XUANKE"},
                                                                    {"id": 2, "name": "K12"},
                                                                    {"id": 8, "name": "ZHUANYE"},
                                                                    {"id": 6, "name": "TIKU"}], "level": "ZHI_YUAN"},
                              "startDateTime": 1650954660000, "endDateTime": 1655274660000, "level": "ZHI_YUAN"},
                             {"id": 96995, "role": {"id": 1, "name": "ZHI_YUAN", "description": "志愿VIP角色",
                                                    "authorities": [{"id": 5, "name": "CEPING"},
                                                                    {"id": 4, "name": "ZHIYUAN"},
                                                                    {"id": 9, "name": "ZHIYE"},
                                                                    {"id": 1, "name": "SHENGYA"},
                                                                    {"id": 7, "name": "YUANXIAO"},
                                                                    {"id": 3, "name": "XUANKE"},
                                                                    {"id": 2, "name": "K12"},
                                                                    {"id": 8, "name": "ZHUANYE"},
                                                                    {"id": 6, "name": "TIKU"}], "level": "ZHI_YUAN"},
                              "startDateTime": 1648799956000, "endDateTime": 1680335956000, "level": "ZHI_YUAN"}],
                   "gotoZhiyuanPage": False,
                   "subjects": [{"id": 1, "name": "物理"}, {"id": 2, "name": "化学"}, {"id": 3, "name": "生物"}],
                   "enrollBatchId": 1024, "platformId": None, "scienceAndArt": "理科"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }

        try:
            res = requests.post("https://wechat.junyanginfo.com/user/users/updateUser", headers=headers,
                                data=json.dumps(payload), verify=False)
            if res.status_code != 200:
                return "zhiyuan-更新用户新高考省份失败，请检查服务"
            province = res.json()['province']['id']
            if province != 430000:
                return "zhiyuan-更新用户新高考省份失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "zhiyuan-更新用户新高考省份失败，请检查服务"

    def update_user_score_ngk(self):
        payload = {"batchId": 1024, "id": 47673, "position": 39282, "provinceId": 430000, "scienceArt": "综合",
                   "score": 550, "subjects": [1, 2, 3]}
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }
        try:
            res = requests.post("https://wechat.junyanginfo.com/zhiyuan/userScore/UpdateScore", headers=headers,
                                data=json.dumps(payload), verify=False)
            if res.status_code != 200:
                return "zhiyuan-新高考修改用户位次失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "zhiyuan-新高考修改用户位次失败，请检查服务"

    def update_user_score_ogk(self):
        payload = {"id": 47673, "scienceArt": "理科", "score": 550, "province": {"id": 530000}, "position": 39282}
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }

        try:
            res = requests.post("https://wechat.junyanginfo.com/zhiyuan/userScore/saveOrUpdateScore", headers=headers,
                                data=json.dumps(payload), verify=False)
            if res.status_code != 200:
                return "zhiyuan-老高考修改用户位次失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "zhiyuan-老高考修改用户位次失败，请检查服务"

    def get_user_enroll_student_plan_ngk(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }

        try:
            res = requests.get(
                "https://wechat.junyanginfo.com/zhiyuan/enrollStudentPlans?page=0&size=10&sortRule=0&probabilityFrom=3&probabilityTo=100&inAlternative=false&projection=alternative&isNewCEE=true&_t=1676279686675",
                headers=headers, verify=False)

            if res.status_code != 200:
                return "zhiyuan-新高考获取用户专业优先招生计划专业列表失败，请检查服务"
            major_name = res.json()['content'][0]['name']
            if not major_name:
                return "zhiyuan-新高考获取用户专业优先招生计划专业列表失败，请检查服务"
            else:
                return False
        except BaseException as e:
            return "zhiyuan-新高考获取用户专业优先招生计划专业列表失败，请检查服务"

    def get_user_enroll_student_plan_group_ngk(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }

        try:
            res = requests.get(
                "https://wechat.junyanginfo.com/zhiyuan/enrollStudentPlanGroups?page=0&size=10&probabilityFrom=3&probabilityTo=100&_=1676279686672&inAlternative=false&isNewCEE=true&pageable=true&_t=1676279686675",
                headers=headers, verify=False)
            if res.status_code != 200:
                return "zhiyuan-新高考获取用户院校优先招生计划专业组列表失败，请检查服务"
            group_name = res.json()['content'][0]['groupName']
            if not group_name:
                return "zhiyuan-新高考获取用户院校优先招生计划专业组列表失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "zhiyuan-新高考获取用户院校优先招生计划专业组列表失败，请检查服务"

    def get_user_college_first_list_ogk(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }
        try:
            res = requests.get(
                "https://wechat.junyanginfo.com/zhiyuan/collegeFirst/queryFirstCollege?page=0&size=10&_=1676515385389&inAlternative=false&_t=1676515385390",
                headers=headers, verify=False)
            if res.status_code != 200:
                return "zhiyuan-老高考获取用户院校优先招生计划列表失败，请检查服务"

            college_name = res.json()['content'][0]['collegeName']
            if not college_name:
                return "zhiyuan-老高考获取用户院校优先招生计划列表失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "zhiyuan-老高考获取用户院校优先招生计划列表失败，请检查服务"

    def get_user_major_first_list_ogk(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }

        try:
            res = requests.get(
                "https://wechat.junyanginfo.com/zhiyuan/enrollStudentPlans?page=0&size=10&inAlternative=false&_t=1676514815954",
                headers=headers, verify=False)
            if res.status_code != 200:
                return "zhiyuan-老高考获取用户专业优先招生计划列表失败，请检查服务"

            major_name = res.json()['content'][0]['name']
            if not major_name:
                return "zhiyuan-老高考获取用户专业优先招生计划列表失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "zhiyuan-老高考获取用户专业优先招生计划列表失败，请检查服务"

    # evaluation
    def ob_top_20(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }
        try:
            res = requests.get(
                "https://wechat.junyanginfo.com/zhiyuan/evaluationMajorResult/obtainNewTopTwentyMajors?userId=53994&_t=1676514063055",
                headers=headers, verify=False)
            if res.status_code != 200:
                return "evaluation-获取测评top20失败，请检查服务"
            major_name = res.json()['popularityCommonList'][0]['name']
            if not major_name:
                return "evaluation-获取测评top20失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "evaluation-获取测评top20失败，请检查服务"

    # content
    def get_xk_book_version(self):
        headers = {
            "Authorization": self._token
        }

        try:
            res = requests.get(
                "https://wechat.junyanginfo.com/content/sxCurriculum/getSyncSxBook?sxBookEditionId=774&page=0&size=100&_t=1676282116494",
                headers=headers)
            if res.status_code != 200:
                return "content-获取升学课堂课程列表失败，请检查服务"

            title = res.json()['content'][0]['title']
            if not title:
                return "content-获取升学课堂课程列表失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "content-获取升学课堂课程列表失败，请检查服务"

    # subject
    def change_subject_province(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }
        payload = {"provinceId": 430000, "provinceName": "湖南", "pattern": "三加一加二", "year": 2024}
        try:
            res = requests.post("https://wechat.junyanginfo.com/xuanke/entranceCollegeMajor/addUserProvinceRecord",
                                headers=headers,
                                data=json.dumps(payload), verify=False)
            if res.status_code != 200:
                return "subject-用户修改省份失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "subject-用户修改省份失败，请检查服务"

    def choose_major_by_subject(self):
        headers = {
            "Authorization": self._token
        }
        try:
            res = requests.get(
                "https://wechat.junyanginfo.com/xuanke/entranceCollegeMajor/queryEntranceSubjectMajor?subject1=1001&subject2=1002&subject3=1004&_t=1676282516480",
                headers=headers,
                verify=False)
            if res.status_code != 200:
                return "subject-返回用户按科目选专业列表失败，请检查服务"
            major_sub_category_name = res.json()['majorCategoryItems'][0]['majorSubCategoryResults'][0][
                'majorSubCategoryName']
            if not major_sub_category_name:
                return "subject-返回用户按科目选专业列表失败，请检查服务"
            else:
                return None
        except BaseException as e:
            return "subject-返回用户按科目选专业列表失败，请检查服务"

    # platform
    @staticmethod
    def platform_login():
        payload = {"username": "test", "password": "test123"}
        headers = {
            "Content-Type": "application/json",
        }
        try:
            res = requests.post(
                "http://platform.zhiyazhiyuan.com/auth/logIn",
                headers=headers, data=json.dumps(payload),
                verify=False)
            if res.status_code != 200:
                return False
            else:
                return True
        except BaseException as e:
            return False

    # oms
    @staticmethod
    def oms_login():
        payload = {"username": "zhongyuan", "password": "zy123456"}
        headers = {
            "Content-Type": "application/json",
        }
        try:
            res = requests.post(
                "https://omsapi.junyanginfo.com/security/login",
                headers=headers, data=json.dumps(payload),
                verify=False)
            if res.status_code != 200:
                return False

            username = res.json()['data']['body']['user']['username']
            if not username:
                return False
            else:
                return True
        except BaseException as e:
            return False

    # enterprise

    def enterprise_login(self):
        payload = {"clientType": "PC", "password": "jy123456", "phoneNumber": "19999900001"}
        headers = {
            "Content-Type": "application/json",

        }

        try:
            res = requests.post(
                "https://wechat.junyanginfo.com/enterprise/registrationAndLogin/byPassword",
                headers=headers, data=json.dumps(payload),
                verify=False)
            if res.status_code != 200:
                return False
            token = res.json()['token']
            self._enterprise_token += token
            if not token:
                return False

            else:
                return True
        except BaseException as e:
            return False

    def enterprise_choose(self):
        payload = {"enterpriseUserId": 354, "userId": 53994}
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._enterprise_token
        }
        res = requests.post(
            "https://wechat.junyanginfo.com/enterprise/registrationAndLogin/login",
            headers=headers, data=json.dumps(payload),
            verify=False)
        if res.status_code != 200:
            return False
        else:
            return True

    # pay.zhiyazhiyuan.com
    @staticmethod
    def pay_web():
        return ServiceMonitor.web_base("https://pay.zhiyazhiyuan.com/",
                                       "wx_open_pay_web-wx_open_pay前端服务未返回200，请检查服务")

    # gaokao.myzhiya.com
    @staticmethod
    def gaokao_web():
        return ServiceMonitor.web_base("http://gaokao.myzhiya.com/",
                                       "gaokao_web-gaokao前端服务未返回200，请检查服务")

    # sale.myzhiya.com
    @staticmethod
    def sale_web():
        return ServiceMonitor.web_base("http://sale.myzhiya.com/",
                                       "sale_web-经销商前端服务未返回200，请检查服务")

    # oms_h5pay
    @staticmethod
    def oms_h5pay_web():
        return ServiceMonitor.web_base("https://activate.zhiyazhiyuan.com/#/index",
                                       "oms_h5pay_web-omsh5支付前端服务未返回200，请检查服务")

    # 生涯评测
    @staticmethod
    def eva_web():
        return ServiceMonitor.web_base("https://eva.zhiyazhiyuan.com/#/index",
                                       "eva_web-生涯评测前端服务未返回200，请检查服务")

    # app下载页
    @staticmethod
    def app_download():
        return ServiceMonitor.web_base("https://app.myzhiya.com/",
                                       "app_download-app下载页前端服务未返回200，请检查服务")

    # xuanke-h5
    @staticmethod
    def xuanke_h5():
        return ServiceMonitor.web_base("http://xuanke.zhiyazhiyuan.com/#/",
                                       "xuanke_h5-h5选科前端服务未返回200，请检查服务")

    # zhiya-teacher
    @staticmethod
    def zhiya_teacher():
        return ServiceMonitor.web_base("http://xk.myzhiya.com/",
                                       "zhiya_teacher-zhiya-teacher前端服务未返回200，请检查服务")

    # 家长评测
    @staticmethod
    def evaluation_web():
        return ServiceMonitor.web_base("http://evaluation.zhiyazhiyuan.com/#/index",
                                       "evaluation_web-家长评测前端服务未返回200，请检查服务")

    # 知涯升学教师端
    @staticmethod
    def teacher_side_web():
        return ServiceMonitor.web_base("https://o.zhiyazhiyuan.com/", "teacher_side_web-知涯升学教师端前端服务未返回200，请检查服务")

    # 教师卡激活
    @staticmethod
    def experience_web():
        return ServiceMonitor.web_base("https://experience.zhiyazhiyuan.com/", "experience_web-教师卡激活前端服务未返回200，请检查服务")

    # 知涯生涯教育学校端管理平台
    @staticmethod
    def saas_web():
        return ServiceMonitor.web_base("http://saas.zhiyazhiyuan.com/", "saas_web-知涯生涯教育学校端管理平台前端服务未返回200，请检查服务")

    # webapp
    @staticmethod
    def webapp():
        return ServiceMonitor.web_base("https://m.zhiyazhiyuan.com/", "webapp-zhiya webapp前端服务未返回200，请检查服务")

    # 机构版前端
    @staticmethod
    def enterprise_web():
        return ServiceMonitor.web_base("https://enterprise.zhiyazhiyuan.com/", "enterprise_web-机构版前端服务未返回200，请检查服务")

    @staticmethod
    def zhiyuan_web():
        return ServiceMonitor.web_base("https://zhiyazhiyuan.com/", "zhiyuan_web-zhiyuan前端服务未返回200，请检查服务")

    @staticmethod
    def oms_web():
        return ServiceMonitor.web_base("https://oms.junyanginfo.com/", "oms_web-oms前端服务未返回200，请检查服务")

    @staticmethod
    def yan_xue_web():
        return ServiceMonitor.web_base("http://yanxue.myzhiya.com/", "yanxue_web-研学前端服务未返回200，请检查服务")

    @staticmethod
    def web_base(url, content):
        try:
            res = requests.get(url, verify=False)
            if res.status_code != 200:
                return content
            else:
                return None
        except:
            return content

    def test_enterprise(self):
        if not self.enterprise_login():
            mail.send_to(subject="enterprise-登录失败，请检查服务")
            return False
        if not self.enterprise_choose():
            mail.send_to(subject="enterprise-选择企业失败，请检查服务")

    def test_oms(self):
        if not self.oms_login():
            mail.send_to(subject="oms-登录失败，请检查服务")

    def test_platform(self):
        if not self.platform_login():
            mail.send_to(subject="platform-登录失败，请检查服务")

    def test_backend(self):
        login_res = self.user_login()
        if not login_res:
            mail.send_to(subject="login-密码登录失败，请检查服务")
            return False
        change_subject_province_res = self.change_subject_province()
        choose_major_by_subject_res = self.choose_major_by_subject()
        get_xk_book_version_res = self.get_xk_book_version()
        ob_top_20_res = self.ob_top_20()
        update_user_province_ogk_res = self.update_user_province_ogk()
        update_user_score_ogk_res = self.update_user_score_ogk()
        get_user_college_first_list_ogk_res = self.get_user_college_first_list_ogk()
        get_user_major_first_list_ogk_res = self.get_user_major_first_list_ogk()
        update_user_province_ngk_res = self.update_user_province_ngk()
        update_user_score_ngk_res = self.update_user_score_ngk()
        get_user_enroll_student_plan_ngk_res = self.get_user_enroll_student_plan_ngk()
        get_user_enroll_student_plan_group_ngk_res = self.get_user_enroll_student_plan_group_ngk()
        mail_content = ""
        if change_subject_province_res:
            mail_content += change_subject_province_res + "\n"
        if choose_major_by_subject_res:
            mail_content += choose_major_by_subject_res + "\n"
        if get_xk_book_version_res:
            mail_content += get_xk_book_version_res + "\n"
        if ob_top_20_res:
            mail_content += ob_top_20_res + "\n"
        if update_user_province_ogk_res:
            mail_content += update_user_province_ogk_res + "\n"
        if update_user_score_ogk_res:
            mail_content += update_user_score_ogk_res + "\n"
        if get_user_college_first_list_ogk_res:
            mail_content += get_user_college_first_list_ogk_res + "\n"
        if get_user_major_first_list_ogk_res:
            mail_content += get_user_major_first_list_ogk_res + "\n"
        if update_user_province_ngk_res:
            mail_content += update_user_province_ngk_res + "\n"
        if update_user_score_ngk_res:
            mail_content += update_user_score_ngk_res + "\n"
        if get_user_enroll_student_plan_ngk_res:
            mail_content += get_user_enroll_student_plan_ngk_res + "\n"
        if get_user_enroll_student_plan_group_ngk_res:
            mail_content += get_user_enroll_student_plan_group_ngk_res + "\n"
        if mail_content:
            mail.send_to(subject="后端服务监控", contents=mail_content)

    def test_front(self):
        pay_web_res = self.pay_web()
        gaokao_web_res = self.gaokao_web()
        sale_web_res = self.sale_web()
        oms_h5pay_web_res = self.oms_h5pay_web()
        eva_web_res = self.eva_web()
        app_download_res = self.app_download()
        xuanke_h5_res = self.xuanke_h5()
        zhiya_teacher_res = self.zhiya_teacher()
        evaluation_web_res = self.evaluation_web()
        teacher_side_web_res = self.teacher_side_web()
        experience_web_res = self.experience_web()
        saas_web_res = self.saas_web()
        webapp_res = self.webapp()
        enterprise_web_res = self.enterprise_web()
        zhiyuan_web_res = self.zhiyuan_web()
        oms_web_res = self.oms_web()
        yan_xue_web_res = self.yan_xue_web()
        mail_content = ""
        if pay_web_res:
            mail_content += pay_web_res + "\n"
        if gaokao_web_res:
            mail_content += gaokao_web_res + "\n"
        if sale_web_res:
            mail_content += sale_web_res + "\n"
        if oms_h5pay_web_res:
            mail_content += oms_h5pay_web_res + "\n"
        if eva_web_res:
            mail_content += eva_web_res + "\n"
        if app_download_res:
            mail_content += app_download_res + "\n"
        if xuanke_h5_res:
            mail_content += xuanke_h5_res + "\n"
        if zhiya_teacher_res:
            mail_content += zhiya_teacher_res + "\n"
        if evaluation_web_res:
            mail_content += evaluation_web_res + "\n"
        if teacher_side_web_res:
            mail_content += teacher_side_web_res + "\n"
        if experience_web_res:
            mail_content += experience_web_res + "\n"
        if saas_web_res:
            mail_content += saas_web_res + "\n"
        if webapp_res:
            mail_content += webapp_res + "\n"
        if enterprise_web_res:
            mail_content += enterprise_web_res
        if zhiyuan_web_res:
            mail_content += zhiyuan_web_res
        if oms_web_res:
            mail_content += oms_web_res
        if yan_xue_web_res:
            mail_content += yan_xue_web_res
        if mail_content:
            mail.send_to(subject="前端服务监控", contents=mail_content)


if __name__ == '__main__':
    obj = ServiceMonitor()
    conf = {
        'host': "159.75.224.137",
        'port': 6399,
        'password': "rYa+wq10dFTWzYz8FeZgsWRygyKfLKULSRdKfRnEgSk=",
        # 'decode_responses': True
    }
    # # # executors = {
    # # #     'default': ThreadPoolExecutor(10),  # 默认线程数
    # # #     'processpool': ProcessPoolExecutor(3)  # 默认进程
    # # # }
    jobstores = {
        'redis': RedisJobStore(db=3, **conf),

    }
    scheduler = BlockingScheduler(jobstores=jobstores, timezone='Asia/Shanghai')
    scheduler.add_job(obj.test_front, 'interval', jobstore='redis', name="front", minutes=10, replace_existing=True)
    scheduler.add_job(obj.test_oms, 'interval', jobstore='redis', name="front", minutes=10, replace_existing=True)
    scheduler.add_job(obj.test_backend, 'interval', jobstore='redis', name="front", minutes=10, replace_existing=True)
    scheduler.add_job(obj.test_enterprise, 'interval', jobstore='redis', name="front", minutes=10,
                      replace_existing=True)
    scheduler.add_job(obj.test_platform, 'interval', jobstore='redis', name="front", minutes=10,
                      replace_existing=True)
    scheduler.start()
