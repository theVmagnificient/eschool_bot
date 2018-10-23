from req import *

class Bot:
    def __init__(self):
        self.nineClMenu = [
            ['Алгебра', 'Английский язык', 'Биология'],
            ['География', 'Геометрия', 'Информатика и ИКТ'],
            ['Искусство', 'История', 'Литература'],
            ['Обществознание', 'Русский язык', 'Физика'],
            ['Физическая культура', 'Химия']
        ]
        self.tenClMenu = [
            ['Алгебра', 'Английский язык', 'Биология'],
            ['Геометрия', 'Информатика и ИКТ'],
            ['История', 'Литература', 'Математический анализ'],
            ['Обществознание', 'ОБЖ', 'Русский язык', 'Физика'],
            ['Физическая культура', 'Физическая лаборатория', 'Химия']
        ]
        self.nineClPeriods = [
            ['1 четверть', '2 четверть', '3 четверть', '4 четверть'],
            ['1 полугодие', '2 полугодие'],
        ]

        self.tenClPeriods = [
            ['1 полугодие', '2 полугодие'],
        ]
        self.echomsg = []  #dict!!
        self.echocmd = []  #dict!!
        self.numberofUsers = 0
        self.dictofUsers = {}
        self.currentPeriod = '1 полугодие'

    def new_user(self, chat_id):
        self.dictofUsers.update({chat_id:User(chat_id)})
    def get_user(self, chat_id):
        return self.dictofUsers.get(chat_id)

class User:
    def __init__(self, chat_id):
        self.sLogin = None
        self.sPassword = None
        self.chat_id = chat_id
        self.user_id = None
        self.Islog = False
        self.IsAdmin = False
        self.ES = EschoolConnectionHandler()
        self.currentPeriod = None
        self.currentSubject = None


    def login(self, login, pas, ishash_pas=False):
        self.sLogin = login
        self.sPassword = pas
        a = self.ES.login(login, pas, ishash_pas=ishash_pas)
        if a == 0:
            self.sLogin = login
            self.sPassword = pas
            a = 1
            self.Class = self.ES.get_user_grade()
            if self.Class == "11 кл" or self.Class == "10 кл":
                self.currentPeriod = "1 полугодие"
            elif self.Class == "5-9 кл":
                self.currentPeriod = "1 четверть"

        else:
            a = 0
        return a



    def push_is_Log(self):
        self.IsLog = True

    def get_is_Log(self):
        return self.IsLog


""""
dict = {}
dict.update({'a':'b'})
dict.update({2:Bot()})
print(dict)
dict[2].numberofUsers = 10
print(dict[2].numberofUsers)
"""

"""
    #bot.send_message(chat_id=update.message.chat_id, text="Привет☺☺☺        Я - бот для удобного использования сервиса eSchool    "
    #                                                      "электронного дневника для зоки.          "
    #                                                      "Для начала работы мне понадобится твой Логин и Пароль:")
    
"""
