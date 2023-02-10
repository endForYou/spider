import requests
import json
from time import sleep
import redis
import urllib3
from junyang_spider.libs.mail import Mail

urllib3.disable_warnings()
mail = Mail()


class ServiceMonitor:

    def __init__(self):
        self._token = "Bearer "

    def user_login(self):
        payload = {
            "phoneNumber": "19999900001",
            "password": "jy123456",
            "clientType": "PC"
        }
        headers = {
            "Content-Type": "application/json",
        }
        res = requests.post("https://wechat.junyanginfo.com/login/byPassword", headers=headers,
                            data=json.dumps(payload))
        try:
            token = res.json()['token']
            self._token += token
        except BaseException as e:
            mail.send_to(subject="密码登录失败，请检查服务")
            # 由于登录失败了，后面的脚本不用执行了
            exit(1)

    def update_user_score_ngk(self):
        payload = {
            "batchId": 1024, "id": 47673, "position": 3928, "provinceId": 430000, "scienceArt": "综合", "score": 550,
            "subjects": [1, 2, 3]
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1Mzk5NCIsImNsaWVudFR5cGUiOiJQQyIsImlhdCI6MTY3NTkwNzc1NH0.QwanX2JFl79GYBAzlfWQGk4Xk69YYQMKQeQhkCaJpjXSO24UsuwjHG-AbH1uQEuKWH_qdklKgnWXfXMkTGNpoQ"
        }
        ret = requests.post("https://wechat.junyanginfo.com/zhiyuan/userScore/UpdateScore", headers=headers,
                            data=json.dumps(payload), verify=False)
        print(ret, ret.text)
        return ret

    def update_user_score_ogk(self):
        payload = {
            "batchId": 1024, "id": 47673, "position": 3928, "provinceId": 430000, "scienceArt": "综合", "score": 550,
            "subjects": [1, 2, 3]
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1Mzk5NCIsImNsaWVudFR5cGUiOiJQQyIsImlhdCI6MTY3NTkwNzc1NH0.QwanX2JFl79GYBAzlfWQGk4Xk69YYQMKQeQhkCaJpjXSO24UsuwjHG-AbH1uQEuKWH_qdklKgnWXfXMkTGNpoQ"
        }
        ret = requests.post("https://wechat.junyanginfo.com/zhiyuan/userScore/UpdateScore", headers=headers,
                            data=json.dumps(payload), verify=False)
        print(ret, ret.text)
        return ret

    def update_user_province(self):
        pass

    def get_user_enrollStudent_plan(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1Mzk5NCIsImNsaWVudFR5cGUiOiJQQyIsImlhdCI6MTY3NTkwNzc1NH0.QwanX2JFl79GYBAzlfWQGk4Xk69YYQMKQeQhkCaJpjXSO24UsuwjHG-AbH1uQEuKWH_qdklKgnWXfXMkTGNpoQ"
        }
        ret = requests.get(
            "https://wechat.junyanginfo.com/zhiyuan/enrollStudentPlans?page=0&size=10&inAlternative=false&projection=alternative&isNewCEE=true&_t=1675929898089",
            headers=headers, verify=False)
        print(ret, ret.text)
        return ret

    def get_user_enroll_student_plan_group(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1Mzk5NCIsImNsaWVudFR5cGUiOiJQQyIsImlhdCI6MTY3NTkwNzc1NH0.QwanX2JFl79GYBAzlfWQGk4Xk69YYQMKQeQhkCaJpjXSO24UsuwjHG-AbH1uQEuKWH_qdklKgnWXfXMkTGNpoQ"
        }
        ret = requests.get(
            "https://wechat.junyanginfo.com/zhiyuan/enrollStudentPlanGroups?page=0&size=10&_=1675930130685&inAlternative=false&isNewCEE=true&pageable=true&_t=1675930130685",
            headers=headers, verify=False)
        print(ret, ret.text)
        return ret

    def user_major_first(self):
        payload = {
            "id": 4803831
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1Mzk5NCIsImNsaWVudFR5cGUiOiJQQyIsImlhdCI6MTY3NTkwNzc1NH0.QwanX2JFl79GYBAzlfWQGk4Xk69YYQMKQeQhkCaJpjXSO24UsuwjHG-AbH1uQEuKWH_qdklKgnWXfXMkTGNpoQ"
        }
        ret = requests.post("https://wechat.junyanginfo.com/zhiyuan/majorFirst", headers=headers,
                            data=json.dumps(payload), verify=False)
        print(ret, ret.text)
        return ret

    def user_alternative(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1Mzk5NCIsImNsaWVudFR5cGUiOiJQQyIsImlhdCI6MTY3NTkwNzc1NH0.QwanX2JFl79GYBAzlfWQGk4Xk69YYQMKQeQhkCaJpjXSO24UsuwjHG-AbH1uQEuKWH_qdklKgnWXfXMkTGNpoQ"
        }
        ret = requests.get(
            "https://wechat.junyanginfo.com/zhiyuan/alternatives?page=0&size=10&probabilityFrom=3&probabilityTo=100&_=1675931729484&projection=group&_t=1675931729488",
            headers=headers, verify=False)
        print(ret, ret.text)
        return ret

    def get_user_item(self):
        payload = {
            "enrollBatchId": 1024,
            "items": [{"sequence": 0,
                       "enrollStudentPlanGroupCode": "1325_001",
                       "items": [{"enrollStudentPlanId": 4802706, "sequence": 0},
                                 {"enrollStudentPlanId": 4809927, "sequence": 1},
                                 {"enrollStudentPlanId": 4818492, "sequence": 2},
                                 {"enrollStudentPlanId": 4815702, "sequence": 3}]}]
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1Mzk5NCIsImNsaWVudFR5cGUiOiJQQyIsImlhdCI6MTY3NTkwNzc1NH0.QwanX2JFl79GYBAzlfWQGk4Xk69YYQMKQeQhkCaJpjXSO24UsuwjHG-AbH1uQEuKWH_qdklKgnWXfXMkTGNpoQ"
        }
        ret = requests.post("https://wechat.junyanginfo.com/zhiyuan/wishEnrollStudentPlans/items", headers=headers,
                            data=json.dumps(payload), verify=False)
        print(ret, ret.text)
        return ret
    # evaluation
    def ob_new_question(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1Mzk5NCIsImNsaWVudFR5cGUiOiJQQyIsImlhdCI6MTY3NTkwNzc1NH0.QwanX2JFl79GYBAzlfWQGk4Xk69YYQMKQeQhkCaJpjXSO24UsuwjHG-AbH1uQEuKWH_qdklKgnWXfXMkTGNpoQ"
        }
        ret = requests.get("https://wechat.junyanginfo.com/evaluation/eval/obtainNewQuestions?_t=1675932777880",
                           headers=headers, verify=False)
        print(ret, ret.text)
        return ret

    # content
    def get_xk_book_version(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }
        res = requests.get("https://wechat.junyanginfo.com/content/xkTextbookVersions/?subjectId=1",
                           headers=headers)

    # subject
    # platform
    # user_center
    # login
    # oms login
    #

if __name__ == '__main__':
    obj=ServiceMonitor()
    # obj.user_login()
#