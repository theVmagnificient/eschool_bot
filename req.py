import requests
import hashlib
from db import *


def get_field_val(text, field, anchor = 0, mode="", endsym = ","):
    if mode == "":
        ind = text.find(field, anchor)
        tmp = text.find(":", ind)
        return ''.join([x for x in text[tmp + 1 : text.find(endsym, ind)] if (x != "\"" and x != "\'")])
    # if anchor is the right bound
    elif mode == "r":
        ind = text.rfind(field, 0, anchor)
        tmp = text.find(":", ind)
        return''.join([x for x in text[tmp + 1: text.find(endsym, ind)] if (x != "\"" and x != "\'")])

    else:
        return "Incorrect mode"

class EschoolConnectionHandler:

    def __init__(self):
        self._userID = None
        self.s = requests.Session()
        self.url = 'https://app.eschool.center/ec-server/login'
        self.hash_pas = None

    def login(self, log, password):
        self.hash_pas = hashlib.sha256(password.encode()).hexdigest()
        p = self.s.post(self.url, data={'username': log,
                                        'password': self.hash_pas})

        if p.status_code == 200:
            return 0
        else:
            return p.status_code

    def get_user_id(self):
        if self._userID:
            return self._userID
        p = self.s.get("https://app.eschool.center/ec-server/state")
        self._userID = get_field_val(p.text, "userId")
        return self._userID

    def get_per_id(self, per_name = "1 полугодие"):
        p = self.s.get("https://app.eschool.center/ec-server/dict/periods2?year=2017")
        anc = p.text.find(per_name, p.text.find(self.get_user_grade()))
        id = get_field_val(p.text, "id", anchor=anc, mode="r")
        return id

    def get_avg_mark(self, subj_name="Алгебра", per_name="1 полугодие"):
        p = self.s.get("https://app.eschool.center/ec-server/student/getDiaryUnits/?userId=" +
                           self.get_user_id() + "&eiId=" + self.get_per_id(per_name))
        anc = p.text.find(subj_name)
        return get_field_val(p.text, "overMark", anc)

    def get_user_grade(self):
        p = self.s.get("https://app.eschool.center/ec-server/usr/groupByUser?userId=" + self.get_user_id())
        grade = get_field_val(p.text, "groupName").split(sep="-")[0]
        if grade == '10':
            grade = '11'
        elif grade != '11':
            grade = '5-9'
        return grade + " кл"


a = EschoolConnectionHandler()

log = input("Log: ")
pas = input("Pas: ")
a.login(log, pas)

print(a.get_user_id())

print(a.get_avg_mark())

print(a.get_user_grade())

DBInstance.init()

DBInstance.push("qwerty", log, a.hash_pas, a.get_user_id())

a = DBInstance.get("qwerty")

DBInstance.update("qwerty", "kek")

b = DBInstance.get("qwerty")

DBInstance.delete("qwerty")

c = DBInstance.get("qwerty")

DBInstance.close()