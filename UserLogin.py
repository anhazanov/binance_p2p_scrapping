import sqlite3, time

from flask import url_for
from flask_login import UserMixin
from db import Database

class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = Database().getUser(user_id)
        return self

    def creat(self, user):
        self.__user = user
        return self

    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False

    def get_id(self):
        return str(self.__user[0])

    def getName(self):
        return self.__user[1] if self.__user else 'Без имени'

    def getEmail(self):
        return self.__user[2] if self.__user else 'Без email'

    def getPay(self):
        return self.__user[-1] if self.__user else False

    def getPayDate(self):
        return time.ctime(self.__user[-1]) if self.__user else False

    def getAvatar(self, app):
        img = None
        if not self.__user[5]:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default_avatar.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию:" + str(e))
        else:
            img = self.__user[5]
        return img

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == 'png' or ext == "PNG":
            return True
        return False

