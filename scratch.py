import requests
import hashlib



url = 'https://app.eschool.center/ec-server/login'


def get_field_val(text, field, anchor = 0, mode="", endsym = ","):
    if mode == "":
        ind = text.find(field, anchor)
        tmp = text.find(":", ind)
        return ''.join([x for x in text[tmp + 1 : text.find(endsym, ind)] if (x != "\"" and x != "\'")])
    # if anchor is the right bound
    elif mode == "r":
        ind = text.rfind(field, 0, anchor)
        tmp = text.find(":", ind)
        return [x for x in text[tmp + 1: text.find(endsym, ind)] if (x != "\"" and x != "\'")]

    else:
        return "Incorrect mode"



payload = {'username': 'kirill_lopatin', 'password': hashlib.sha256("Lopatin7676".encode()).hexdigest()}
with requests.Session() as s:

    p = s.post(url, data=payload)
    # print the html returned or something more intelligent to see if it's a successful login page.

    #p = s.get("https://app.eschool.center/#/Private/studentMarks")
    p = s.get("https://app.eschool.center/ec-server/state")

    anc = p.text.find("\"userId\":")
    userId = p.text[anc + 9 : p.text.find(",", anc)]

    p = s.get("https://app.eschool.center/ec-server/dict/periods2?year=2017")

    # find period id
    anc = p.text.rfind("\"id\":", 0, p.text.find("1 полугодие", p.text.find("11 кл")))
    perId = p.text[anc + 5 : p.text.find(",", anc)]

    p = s.get("https://app.eschool.center/ec-server/student/getDiaryUnits/?userId=" + userId + "&eiId=" + perId)

    lesName = input("Lesson name: ")

    anc = p.text.find(lesName)

    overMark = get_field_val(p.text, "overMark", anc)

    print(p.text)