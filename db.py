from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
    chatId = CharField()
    login = CharField()
    password = CharField()
    userId = CharField()

    class Meta:
        database = db  # This model uses the "people.db" database.


class DBInstance:
    @staticmethod
    def init():
        db.connect()
        db.create_tables([Person])

    @staticmethod
    def push(chatid, login, password, userid):
        Person.create(chatId=chatid, login=login, password=password, userId=userid)

    @staticmethod
    def update(chatid, login = "", password = ""):
        query = Person.select().where(Person.chatId == chatid)
        if query.exists():
            user = Person.get(Person.chatId == chatid)
            if login != "":
                user.login = login
            if password != "":
                user.password = password
            user.save()

    @staticmethod
    def delete(chatid):
        query = Person.select().where(Person.chatId == chatid)
        if query.exists():
            a = Person.get(Person.chatId == chatid).delete_instance()
            print(a)

    @staticmethod
    def get(chatid):
        query = Person.select().where(Person.chatId == chatid)
        if query.exists():
             return Person.get(Person.chatId == chatid)
        else:
            return "User doesn't exist"

    @staticmethod
    def close():
        db.close()
