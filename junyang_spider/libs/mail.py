import yagmail


class Mail:
    def __init__(self):
        self._server = yagmail.SMTP(user='jiewei1989830@sina.com', password='bf3fd9b21d632dd7', host='smtp.sina.com')
        self._recipients = ["jiewei@junyanginfo.com", "dev@junyanginfo.com", "zhongyuan@junyanginfo.com"]

    def send_to(self, subject="just from endaqa", contents="default content"):
        try:
            self._server.send(to=self._recipients, subject=subject, contents=contents)
        except BaseException as e:
            print("send mail failed! ", e)
