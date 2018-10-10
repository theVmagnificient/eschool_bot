import requests
import hashlib
import re
import datetime
from db import *


def get_field_val(text, field, anchor = 0, mode="", endsym = ","):
    if mode == "":
        ind = text.find(field, anchor)
        tmp = text.find(":", ind)
        return ''.join([x for x in text[tmp + 1: text.find(endsym, ind)] if (x != "\"" and x != "\'")])
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

    def get_per_id(self, per_name="1 полугодие"):
        cl = self.get_user_grade()
        if cl == "11 кл" or cl == "10 кл":
            if per_name.find("полугодие") > 0:
                per_name = per_name.replace("полугодие", "семестр")
                
        p = self.s.get("https://app.eschool.center/ec-server/dict/periods2?year=2018")
        anc = p.text.find(per_name, p.text.find(self.get_user_grade()))
        if anc == -1:
            anc = p.text.rfind(per_name, p.text.find(self.get_user_grade()))
        
        id = get_field_val(p.text, "id", anchor=anc, mode="r")
        return id

    def get_avg_mark(self, subj_name="Физика", per_name="1 полугодие"):
        cl = self.get_user_grade()
        if cl == "11 кл" or cl == "10 кл":
            if per_name.find("полугодие") > 0:
                per_name = per_name.replace("полугодие", "семестр")
        p = self.s.get("https://app.eschool.center/ec-server/student/getDiaryUnits/?userId=" +
                           self.get_user_id() + "&eiId=" + self.get_per_id(per_name))
        anc = p.text.find(subj_name)
        return get_field_val(p.text, "overMark", anc)

    def get_class_by_id(self, subj_id, per_name="1 полугодие"):
        p = self.s.get("https://app.eschool.center/ec-server/student/getDiaryUnits/?userId=" +
                       self.get_user_id() + "&eiId=" + self.get_per_id(per_name))
        anc = p.text.find("unitId\":" + str(subj_id))
        return get_field_val(p.text, "unitName", anc, mode="r")
        

    def get_user_grade(self):
        p = self.s.get("https://app.eschool.center/ec-server/usr/groupByUser?userId=" + self.get_user_id())
        grade = get_field_val(p.text, "groupName").split(sep="-")[0]
        if grade != '11' and grade != '10':
            grade = '5-9'
        return grade + " кл"

    def get_new_marks(self, per_name="1 полугодие"):
        p = self.s.get("https://app.eschool.center/ec-server/student/getDiaryPeriod/?userId=" +
                       self.get_user_id() + "&eiId=" + self.get_per_id(per_name))
        now = datetime.datetime.now()
    
        for k in range(8):
            t = 7 - k
            d = datetime.date(now.year, now.month, now.day) - datetime.timedelta(days=t)     # d = datetime.today() - timedelta(days=26)
            s = "markDate\":" + "\"" + str(d)

            for i in [m.start() for m in re.finditer(s, p.text)]:
                left = p.text.rfind("{", 0, i)
                right = p.text.find("}", i)
                a = p.text[left:right]

                isUpdated = get_field_val(a, "isUpdated", 0)
                if isUpdated == '1':
                    print("Mark:" + get_field_val(a, "markVal", 0))
                    print("Class:" + self.get_class_by_id(get_field_val(a, "unitId", 0)))
                    print("Name: " + get_field_val(a, "lptName", 0))
                    print("Weight: " + get_field_val(a, "mktWt", 0))
                    print("Date: " + str(d))
                    print("_________________________________")

        
        


